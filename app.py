# Dash dependencies
import dash
import dash_bootstrap_components as dbc

import flask
# Plotly custom theme
import plotly.io as pio
from assets import plotly_theme
pio.templates.default = "cadlabs_frontend"

# Import layout components
from layout.layout import layout

from dash.dependencies import Input, Output, State
import plotly.express as px
import copy
import pandas as pd
import numpy as np

from model.system_parameters import parameters
from experiments.base import experiment
from experiments.run import run
from experiments.post_processing import post_process
from model.types import Percentage

from utils.visualizations import plot_revenue_yields_vs_network_inflation


server = flask.Flask(__name__) # define flask app.server


app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.LUX])
    
app.title = "Eth2 Calculator"
app.layout = layout

# Callbacks
@app.callback(
    Output("collapse-eth2", "is_open"),
    [Input("collapse-button-eth2", "n_clicks")],
    [State("collapse-eth2", "is_open")],
)
def toggle_collapse_eth2(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("BASE_REWARD_FACTOR", "value"),
    Output("MAX_EFFECTIVE_BALANCE", "value"),
    Output("EFFECTIVE_BALANCE_INCREMENT", "value"),
    Output("PROPOSER_REWARD_QUOTIENT", "value"),
    Output("WHISTLEBLOWER_REWARD_QUOTIENT", "value"),
    Output("MIN_SLASHING_PENALTY_QUOTIENT", "value"),
    [Input("button-eth2-specs-default", "n_clicks")]
)
def load_eth2_specs_defaults(n_clicks):
    base_reward_factor = parameters['BASE_REWARD_FACTOR'][0]
    max_effective_balance = parameters['MAX_EFFECTIVE_BALANCE'][0]/1e9
    effective_balance_increment = parameters['EFFECTIVE_BALANCE_INCREMENT'][0]/1e9
    proposer_reward_quotient = parameters['PROPOSER_REWARD_QUOTIENT'][0]
    whistleblower_reward_quotient = parameters['WHISTLEBLOWER_REWARD_QUOTIENT'][0]
    min_slashing_penalty_quotient = parameters['MIN_SLASHING_PENALTY_QUOTIENT'][0]

    return (base_reward_factor, 
            max_effective_balance, effective_balance_increment, proposer_reward_quotient,
            whistleblower_reward_quotient, min_slashing_penalty_quotient)

@app.callback(
    Output("collapse-validator", "is_open"),
    [Input("collapse-button-validator", "n_clicks")],
    [State("collapse-validator", "is_open")],
)
def toggle_collapse_validator(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("validator_internet_uptime", "value"),
    Output("diy_hardware_distribution", "value"),
    Output("diy_cloud_distribution", "value"),
    Output("pool_staas_distribution", "value"),
    Output("pool_hardware_distribution", "value"),
    Output("pool_cloud_distribution", "value"),
    Output("staas_full_distribution", "value"),
    Output("staas_self_custodied_distribution", "value"),
    Output("diy_hardware_cost", "value"),
    Output("diy_cloud_cost", "value"),
    Output("pool_staas_cost", "value"),
    Output("pool_hardware_cost", "value"),
    Output("pool_cloud_cost", "value"),
    Output("staas_full_cost", "value"),
    Output("staas_self_custodied_cost", "value"),
    Output("validator_distribution_weighted_avg_cost", "value"),
    [Input("button-validator-specs-default", "n_clicks")]
)
def load_validator_specs_defaults(n_clicks):
    validator_internet_uptime = 100 * parameters['validator_uptime_process'][0](0,0)
    diy_hardware_distribution = 100 * parameters['validator_percentage_distribution'][0][0]
    diy_cloud_distribution = 100 * parameters['validator_percentage_distribution'][0][1]
    pool_staas_distribution = 100 * parameters['validator_percentage_distribution'][0][2]
    pool_hardware_distribution = 100 * parameters['validator_percentage_distribution'][0][3]
    pool_cloud_distribution = 100 * parameters['validator_percentage_distribution'][0][4]
    staas_full_distribution = 100 * parameters['validator_percentage_distribution'][0][5]
    staas_self_custodied_distribution = 100 * parameters['validator_percentage_distribution'][0][6]

    diy_hardware_cost = parameters['validator_hardware_costs_per_epoch'][0][0]
    diy_cloud_cost = parameters['validator_cloud_costs_per_epoch'][0][1]
    pool_staas_cost = parameters['validator_third_party_costs_per_epoch'][0][2]
    pool_hardware_cost = parameters['validator_hardware_costs_per_epoch'][0][3]
    pool_cloud_cost = parameters['validator_cloud_costs_per_epoch'][0][4]
    staas_full_cost = parameters['validator_third_party_costs_per_epoch'][0][5]
    staas_self_custodied_cost = parameters['validator_third_party_costs_per_epoch'][0][6]
    validator_distribution_weighted_avg_cost = sum([diy_hardware_distribution * diy_hardware_cost,
                                                    diy_cloud_distribution * diy_cloud_cost, 
                                                    pool_staas_distribution * pool_staas_cost,
                                                    pool_hardware_distribution * pool_hardware_cost,
                                                    pool_cloud_distribution * pool_cloud_cost,
                                                    staas_full_distribution * staas_full_cost,
                                                    staas_self_custodied_distribution * staas_self_custodied_cost
                                                    ])/100

    return (validator_internet_uptime, 
            diy_hardware_distribution,
            diy_cloud_distribution, pool_staas_distribution,
            pool_hardware_distribution, pool_cloud_distribution,
            staas_full_distribution, staas_self_custodied_distribution,
            diy_hardware_cost, diy_cloud_cost,
            pool_staas_cost, pool_hardware_cost, pool_cloud_cost,
            staas_full_cost, staas_self_custodied_cost,
            validator_distribution_weighted_avg_cost)


@app.callback(
    Output("validator_total_distribution", "value"),
    [Input("diy_hardware_distribution", "value"),
    Input("diy_cloud_distribution", "value"),
    Input("pool_staas_distribution", "value"),
    Input("pool_hardware_distribution", "value"),
    Input("pool_cloud_distribution", "value"),
    Input("staas_full_distribution", "value"),
    Input("staas_self_custodied_distribution", "value")]
)
def calc_total_validator_distribution(diy_hardware_distribution,
                                      diy_cloud_distribution,
                                      pool_staas_distribution,
                                      pool_hardware_distribution,
                                      pool_cloud_distribution,
                                      staas_full_distribution,
                                      staas_self_custodied_distribution):

    validator_distribution = [diy_hardware_distribution,
                                        diy_cloud_distribution, 
                                        pool_staas_distribution,
                                        pool_hardware_distribution,
                                        pool_cloud_distribution,
                                        staas_full_distribution,
                                        staas_self_custodied_distribution]
 
    non_empty_validators = list(filter(None, validator_distribution))
    validator_total_distribution = sum(non_empty_validators)

    return validator_total_distribution

@app.callback(
    Output("eth_yield_graph", "figure"),
    Output("eth_rewards_graph", "figure"),
    Output("eth_revenue_network_costs_graph", "figure"),
    Output("eth_revenue_profit_graph", "figure"),
    [Input("button-run-simulation", "n_clicks")],
    [State("BASE_REWARD_FACTOR", "value"),
    State("MAX_EFFECTIVE_BALANCE", "value"),
    State("EFFECTIVE_BALANCE_INCREMENT", "value"),
    State("PROPOSER_REWARD_QUOTIENT", "value"),
    State("WHISTLEBLOWER_REWARD_QUOTIENT", "value"),
    State("MIN_SLASHING_PENALTY_QUOTIENT", "value"),      
    State("validator_internet_uptime", "value"),
    State("diy_hardware_distribution", "value"),
    State("diy_cloud_distribution", "value"),
    State("pool_staas_distribution", "value"),
    State("pool_hardware_distribution", "value"),
    State("pool_cloud_distribution", "value"),
    State("staas_full_distribution", "value"),
    State("staas_self_custodied_distribution", "value"),
    State("diy_hardware_cost", "value"),
    State("diy_cloud_cost", "value"),
    State("pool_staas_cost", "value"),
    State("pool_hardware_cost", "value"),
    State("pool_cloud_cost", "value"),
    State("staas_full_cost", "value"),
    State("staas_self_custodied_cost", "value"),
    State("eth_yield_graph", "figure"),
    State("eth_rewards_graph", "figure"),
    State("eth_revenue_network_costs_graph", "figure"),
    State("eth_revenue_profit_graph", "figure")],
)
def run_simulation(n_clicks, BASE_REWARD_FACTOR, 
                   MAX_EFFECTIVE_BALANCE, EFFECTIVE_BALANCE_INCREMENT,
                   PROPOSER_REWARD_QUOTIENT, WHISTLEBLOWER_REWARD_QUOTIENT,
                   MIN_SLASHING_PENALTY_QUOTIENT,
                   validator_internet_uptime,
                   diy_hardware_distribution,
                   diy_cloud_distribution, pool_staas_distribution,
                   pool_hardware_distribution, pool_cloud_distribution,
                   staas_full_distribution, staas_self_custodied_distribution,
                   diy_hardware_cost, diy_cloud_cost, pool_staas_cost,
                   pool_hardware_cost, pool_cloud_cost, staas_full_cost,
                   staas_self_custodied_cost, eth_yield_graph,
                   eth_rewards_graph, eth_revenue_network_costs_graph,
                   eth_revenue_profit_graph):
    if n_clicks is not None:
        selected_parameters = copy.deepcopy(parameters)
        selected_parameters['BASE_REWARD_FACTOR'] = [BASE_REWARD_FACTOR]
        selected_parameters['MAX_EFFECTIVE_BALANCE'] = [1e9 * MAX_EFFECTIVE_BALANCE]
        selected_parameters['EFFECTIVE_BALANCE_INCREMENT'] = [1e9 * EFFECTIVE_BALANCE_INCREMENT]
        selected_parameters['PROPOSER_REWARD_QUOTIENT'] = [PROPOSER_REWARD_QUOTIENT]
        selected_parameters['WHISTLEBLOWER_REWARD_QUOTIENT'] = [WHISTLEBLOWER_REWARD_QUOTIENT]
        selected_parameters['MIN_SLASHING_PENALTY_QUOTIENT'] = [MIN_SLASHING_PENALTY_QUOTIENT]

        selected_parameters['validator_internet_uptime'] = [round(validator_internet_uptime/100,4)]

        selected_parameters['validator_percentage_distribution'] = [np.array([diy_hardware_distribution,
                                                                            diy_cloud_distribution,
                                                                            pool_staas_distribution,
                                                                            pool_hardware_distribution,
                                                                            pool_cloud_distribution,
                                                                            staas_full_distribution,
                                                                            staas_self_custodied_distribution],
                                                                            dtype=Percentage)/100]

        selected_parameters['validator_hardware_costs_per_epoch'] = [np.array([diy_hardware_cost, 0, 0,
                                                                               pool_hardware_cost, 0, 0, 0],
                                                                               dtype=Percentage)]

        selected_parameters['validator_cloud_costs_per_epoch'] = [np.array([0, diy_cloud_cost, 0,
                                                                               0, pool_cloud_cost, 0, 0],
                                                                               dtype=Percentage)]
        
        selected_parameters['validator_third_party_costs_per_epoch'] = [np.array([0, 0, pool_staas_cost,
                                                                               0, 0,staas_full_cost,
                                                                               staas_self_custodied_cost],
                                                                               dtype=Percentage)]
        results, exceptions = run(experiment=experiment)
        df = pd.DataFrame(results)
        df = df.drop(df.query('timestep == 0').index)
        df = post_process(df)
        df['total_revenue_yields_%'] = df['total_revenue_yields'] * 100
        df['total_profit_yields_%'] = df['total_profit_yields'] * 100

        eth_yield_graph = px.line(df, x='timestep', y=['total_revenue_yields_%', 'total_profit_yields_%'])
        eth_yield_graph.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="right",x=0.99))
        
        eth_rewards_graph = plot_revenue_yields_vs_network_inflation(df)
        eth_rewards_graph.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))

        eth_revenue_network_costs_graph = px.line(df, x='timestep', y=['total_revenue', 'total_network_costs'])
        eth_revenue_network_costs_graph.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))

        eth_revenue_profit_graph = px.line(df, x='timestep', y=['total_revenue', 'total_profit'])
        eth_revenue_profit_graph.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))
        
    return (eth_yield_graph, eth_rewards_graph, eth_revenue_network_costs_graph,
            eth_revenue_profit_graph)


if __name__ == '__main__':
    app.run_server(debug=True)
