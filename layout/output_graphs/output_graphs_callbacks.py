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

from app import app
from utils.visualizations import plot_revenue_yields_vs_network_inflation



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
