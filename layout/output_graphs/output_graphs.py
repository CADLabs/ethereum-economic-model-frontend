import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
# Load initial charts from csv file
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


output_graphs = html.Div([
        html.H1('Graph', style={"color": "white"}),
        html.Hr(className="under-title"),
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