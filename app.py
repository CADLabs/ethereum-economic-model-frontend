# Dash dependencies
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_auth
import os
from dotenv import load_dotenv

import pandas as pd
import numpy as np
import copy

from model.system_parameters import parameters
from experiments.base import experiment
from experiments.run import run
from experiments.post_processing import post_process
from model.types import Percentage

# Plotting dependencies
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pd.options.plotting.backend = "plotly"

load_dotenv()
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
VALID_USERNAME_PASSWORD_PAIRS = {
    USERNAME: PASSWORD
}

CONTENT_STYLE = {
    "padding-top": "6rem",
    "padding-bottom": "4rem",
    "background-image": "linear-gradient(#2b6555, #171e27)"
}


def plot_revenue_yields_vs_network_inflation(df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    df_subset_0 = df.query("subset == 0")
    df_subset_1 = df.query("subset == 1")

    # Add traces
    fig.add_trace(
        go.Scatter(x=df_subset_0.timestep, y=df_subset_0.total_revenue_yields_pct, name="Revenue yields (%)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_subset_0.timestep, y=df_subset_0.total_profit_yields_pct, name="Net yields @ 25 (%)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_subset_1.timestep, y=df_subset_1.total_profit_yields_pct, name="Net yields @ 1500 (%)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_subset_0.timestep, y=df_subset_0.supply_inflation_pct, name="ETH Supply inflation (%)"),
        secondary_y=True,
    )


    # Set x-axis title
    fig.update_xaxes(title_text="Epochs")

    # Set y-axes titles
    fig.update_yaxes(title_text="Revenue Yields", secondary_y=False)
    fig.update_yaxes(title_text="Network Inflation Rate (Annualized)", secondary_y=True)
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server

initial_df = pd.read_csv('data/data.csv', index_col=0)
initial_df['total_revenue_yields_%'] = initial_df['total_revenue_yields'] * 100
initial_df['total_profit_yields_%'] = initial_df['total_profit_yields'] * 100

fig_eth_yield = px.line(initial_df, x='timestep', y=['total_revenue_yields_%', 'total_profit_yields_%'])
fig_eth_yield.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="right",x=0.99))

fig_rewards = px.area(initial_df, x='timestep', y=['source_reward', 'target_reward', 'head_reward', 'block_attester_reward', 'block_proposer_reward'])
fig_rewards.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))

fig_eth_revenue_network_costs = px.line(initial_df, x='timestep', y=['total_revenue', 'total_network_costs'])
fig_eth_revenue_network_costs.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))

fig_eth_revenue_profit = px.line(initial_df, x='timestep', y=['total_revenue', 'total_profit'])
fig_eth_revenue_profit.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))
        
exogenous_processes = html.Div(
    [
        html.H3('Exogenous Processes', style={"color": "white"}),
        html.Hr(style={"background-color": "#43b170"}),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="eth_price", type="number", placeholder=" "),
                dbc.Label("Eth price (USD)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="eth_staked", type="number", placeholder=" "),
                dbc.Label("Eth Staked")], className="input-label-float")]),

                dbc.Col([
                dbc.Button("Open eth2 specs",
                            id="collapse-button-eth2",
                            className="button")]),

                dbc.Col([
                dbc.Button("Open validator specs",
                            id="collapse-button-validator",
                            className="button")]),

                dbc.Col([
                dbc.Button("Run simulation",
                            id="button-run-simulation",
                            className="button")])
            ], justify="start"
        ),
    ]
)

eth2_specs = html.Div(
    [
        dbc.Collapse([
        html.Hr(),
        html.H3('Eth2 Specs', style={"color": "white"}),
        html.Hr(style={"background-color": "#43b170"}),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="BASE_REWARD_FACTOR", type="number", placeholder=" "),
                dbc.Label("Base reward factor")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="BASE_REWARDS_PER_EPOCH", type="number", placeholder=" "),
                dbc.Label("Base rewards per epoch")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="MAX_EFFECTIVE_BALANCE", type="number", placeholder=" "),
                dbc.Label("Max effective balance (ETH)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="EFFECTIVE_BALANCE_INCREMENT", type="number", placeholder=" "),
                dbc.Label("Effective balance increment (ETH)")], className="input-label-float")]),
            ], justify="start"
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="PROPOSER_REWARD_QUOTIENT", type="number", placeholder=" "),
                dbc.Label("Proposer reward quotient")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="WHISTLEBLOWER_REWARD_QUOTIENT", type="number", placeholder=" "),
                dbc.Label("Whistleblower reward quotient")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="MIN_SLASHING_PENALTY_QUOTIENT", type="number", placeholder=" "),
                dbc.Label("Min slashing penalty quotient")], className="input-label-float")]),

                dbc.Col([
                dbc.Button("Use default values",
                            id="button-eth2-specs-default",
                            className="button")])
            ], justify="start"
        )],id="collapse-eth2")
    ]   
)

validator_uptime = html.Div(
    [
        html.H3('Validator Parameters', style={"color": "white"}),
        html.Hr(style={"background-color": "#43b170"}),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="validator_internet_uptime", type="number", placeholder=" "),
                dbc.Label("Validator internet uptime (%)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="validator_power_uptime", type="number", placeholder=" "),
                dbc.Label("Validator power uptime (%)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="validator_technical_uptime", type="number", placeholder=" "),
                dbc.Label("Validator technical uptime (%)")], className="input-label-float")]),

                dbc.Col([
                dbc.Button("Use default values",
                            id="button-validator-specs-default",
                            className="button")])
            ], justify="start"
        ),
    ]
)

validator_percentage_distribution = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                dbc.Card([    
                html.H4('Validators distribution', style={"color": "white"}), 
                dbc.Row([
                    html.Div([
                    dbc.Input(id="diy_hardware_distribution", type="number", placeholder=" "),
                    dbc.Label("DIY hardware (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="diy_cloud_distribution", type="number", placeholder=" "),
                    dbc.Label("DIY cloud (%)")], className="input-label-float", style={"width":"200px"})
                ], justify="around"),
                dbc.Row([
                    html.Div([
                    dbc.Input(id="pool_staas_distribution", type="number", placeholder=" "),
                    dbc.Label("Pool StaaS (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="pool_hardware_distribution", type="number", placeholder=" "),
                    dbc.Label("Pool hardware (%)")], className="input-label-float", style={"width":"200px"})
                ], justify="around"),
                dbc.Row([
                    html.Div([
                    dbc.Input(id="pool_cloud_distribution", type="number", placeholder=" "),
                    dbc.Label("Pool cloud (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="staas_full_distribution", type="number", placeholder=" "),
                    dbc.Label("StaaS full (%)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                dbc.Row([
                    html.Div([
                    dbc.Input(id="staas_self_custodied_distribution", type="number", placeholder=" "),
                    dbc.Label("StaaS self custodied (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="validator_total_distribution", type="number", placeholder=" "),
                    dbc.Label("Total(%)")], className="input-label-float", style={"width":"200px"})
                ], justify="around"),
                ], className="validator-card")]),

                dbc.Col([
                    dbc.Card([    
                    html.H4('Validation cost', style={"color": "white"}), 
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="diy_hardware_cost", type="number", placeholder=" "),
                        dbc.Label("DIY hardware ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="diy_cloud_cost", type="number", placeholder=" "),
                        dbc.Label("DIY cloud ($)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="pool_staas_cost", type="number", placeholder=" "),
                        dbc.Label("Pool StaaS ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="pool_hardware_cost", type="number", placeholder=" "),
                        dbc.Label("Pool hardware ($)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="pool_cloud_cost", type="number", placeholder=" "),
                        dbc.Label("Pool cloud ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="staas_full_cost", type="number", placeholder=" "),
                        dbc.Label("StaaS full ($)")], className="input-label-float", style={"width":"200px"})
                        ], justify="around"),
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="staas_self_custodied_cost", type="number", placeholder=" "),
                        dbc.Label("StaaS self custodied ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="validator_distribution_weighted_avg_cost", type="number", placeholder=" "),
                        dbc.Label("Weighted average cost ($)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                    ], className="validator-card")]),
            ]
        )
    ]
)

eip1559 = html.Div(
    [
        html.H3('EIP1559', style={"color": "white"}),
        html.Hr(style={"background-color": "#43b170"}),
        dbc.Row(
            [
                dbc.Col([
                dbc.Input(id="test_3", type="text", placeholder="Eth Price")]),
                dbc.Col([
                dbc.Input(id="test_4", type="text", placeholder="Eth Staked")]),
            ], justify="start"
        ),
    ]
)

output_graphs = html.Div([
        html.H1('Graph', style={"color": "white"}),
        html.Hr(style={"background-color": "#43b170"}),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='eth_yield_graph', figure=fig_eth_yield),
            ]),
            dbc.Col([
                dcc.Graph(id='eth_rewards_graph', figure=fig_rewards),
            ]),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='eth_revenue_network_costs_graph', figure=fig_eth_revenue_network_costs),
            ]),
            dbc.Col([
                dcc.Graph(id='eth_revenue_profit_graph', figure=fig_eth_revenue_profit),
            ]),
        ])
])

card_graph = dbc.Card(
    dbc.FormGroup(
        [
        exogenous_processes,
        eth2_specs,
        dbc.Collapse([
        html.Hr(),
        validator_uptime,
        html.Hr(),
        validator_percentage_distribution], id="collapse-validator"),
        html.Hr(),
        output_graphs
        ]
), body=True, color="#1a2c33")

app.layout = html.Div([
    dbc.Row([dbc.Col(html.H1("Eth2 Staking Calculator", style={"color": "white"}), width=10)], justify="around"),
    dbc.Row([dbc.Col(card_graph, width=10)], justify="around"),  # justify="start", "center", "end", "between", "around"
],
   style=CONTENT_STYLE
)


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
    Output("collapse-validator", "is_open"),
    [Input("collapse-button-validator", "n_clicks")],
    [State("collapse-validator", "is_open")],
)
def toggle_collapse_validator(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("BASE_REWARD_FACTOR", "value"),
    #Output("BASE_REWARDS_PER_EPOCH", "value"),
    Output("MAX_EFFECTIVE_BALANCE", "value"),
    Output("EFFECTIVE_BALANCE_INCREMENT", "value"),
    Output("PROPOSER_REWARD_QUOTIENT", "value"),
    Output("WHISTLEBLOWER_REWARD_QUOTIENT", "value"),
    Output("MIN_SLASHING_PENALTY_QUOTIENT", "value"),
    [Input("button-eth2-specs-default", "n_clicks")]
)
def load_eth2_specs_defaults(n_clicks):
    base_reward_factor = parameters['BASE_REWARD_FACTOR'][0]
    #base_rewards_per_epoch = parameters['BASE_REWARDS_PER_EPOCH'][0]
    max_effective_balance = parameters['MAX_EFFECTIVE_BALANCE'][0]/1e9
    effective_balance_increment = parameters['EFFECTIVE_BALANCE_INCREMENT'][0]/1e9
    proposer_reward_quotient = parameters['PROPOSER_REWARD_QUOTIENT'][0]
    whistleblower_reward_quotient = parameters['WHISTLEBLOWER_REWARD_QUOTIENT'][0]
    min_slashing_penalty_quotient = parameters['MIN_SLASHING_PENALTY_QUOTIENT'][0]

    return (base_reward_factor, 
            #base_rewards_per_epoch, 
            max_effective_balance, effective_balance_increment, proposer_reward_quotient,
            whistleblower_reward_quotient, min_slashing_penalty_quotient)


@app.callback(
    Output("validator_internet_uptime", "value"),
    #Output("validator_power_uptime", "value"),
    #Output("validator_technical_uptime", "value"),
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
    #validator_power_uptime = 100 * parameters['validator_power_uptime'][0]
    #validator_technical_uptime = 100 * parameters['validator_technical_uptime'][0]
    
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
            #validator_power_uptime, validator_technical_uptime, 
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
    #State("BASE_REWARDS_PER_EPOCH", "value"),
    State("MAX_EFFECTIVE_BALANCE", "value"),
    State("EFFECTIVE_BALANCE_INCREMENT", "value"),

    State("PROPOSER_REWARD_QUOTIENT", "value"),
    State("WHISTLEBLOWER_REWARD_QUOTIENT", "value"),
    State("MIN_SLASHING_PENALTY_QUOTIENT", "value"),
        
    State("validator_internet_uptime", "value"),
    #State("validator_power_uptime", "value"),
    #State("validator_technical_uptime", "value"),
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
                   #BASE_REWARDS_PER_EPOCH,
                   MAX_EFFECTIVE_BALANCE, EFFECTIVE_BALANCE_INCREMENT,
                   PROPOSER_REWARD_QUOTIENT, WHISTLEBLOWER_REWARD_QUOTIENT,
                   MIN_SLASHING_PENALTY_QUOTIENT,
                   validator_internet_uptime,
                   #validator_power_uptime,
                   #validator_technical_uptime,
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
        #selected_parameters['BASE_REWARDS_PER_EPOCH'] = [BASE_REWARDS_PER_EPOCH]
        selected_parameters['MAX_EFFECTIVE_BALANCE'] = [1e9 * MAX_EFFECTIVE_BALANCE]
        selected_parameters['EFFECTIVE_BALANCE_INCREMENT'] = [1e9 * EFFECTIVE_BALANCE_INCREMENT]
        selected_parameters['PROPOSER_REWARD_QUOTIENT'] = [PROPOSER_REWARD_QUOTIENT]
        selected_parameters['WHISTLEBLOWER_REWARD_QUOTIENT'] = [WHISTLEBLOWER_REWARD_QUOTIENT]
        selected_parameters['MIN_SLASHING_PENALTY_QUOTIENT'] = [MIN_SLASHING_PENALTY_QUOTIENT]

        selected_parameters['validator_internet_uptime'] = [round(validator_internet_uptime/100,4)]
        #selected_parameters['validator_power_uptime'] = [round(validator_power_uptime/100, 4)]
        #selected_parameters['validator_technical_uptime'] = [round(validator_technical_uptime/100, 4)]

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
    

if __name__ == "__main__":
    app.run_server(debug=True)
