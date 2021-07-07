import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes

"""
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
), body=True, color="#272838")

layout_old = html.Div([
    dbc.Row([dbc.Col(html.H1("Eth2 Staking Calculator", style={"color": "white"}), width=10)], justify="around"),
    dbc.Row([dbc.Col(card_graph, width=10)], justify="around"),
],className="outer-background")
"""

layout = html.Div([
    html.Div([
        html.Label([
        "Validator Adoption Scenario",
        dcc.Dropdown(
            id='validator-dropdown', clearable=False,
            value='3', options=[
                {'label': 'Normal Adoption', 'value': 3},
                {'label': 'Low Adoption', 'value': 3 * 0.5},
                {'label': 'High Adoption', 'value': 3 * 1.5},
                {'label': 'Custom', 'value': 'Custom'}
            ]),
            html.Label([
            "Validator Adoption",
            dcc.Slider(
            id='validator-adoption-slider',
            min=0,
            max=10,
            step=0.5,
            marks={
                0: '0',
                5: '5',
                10: '10',
            },
            value=3,
            tooltip={'placement':'top'}
        )]),
            ], style={'background-color': '#272838', 'float':'left', 'width': '25%', 'height': '50px'}),
        html.Label([
        "PoS Launch Date",
        dcc.Dropdown(
            id='pos-launch-date-dropdown', clearable=False,
            value='2021/12/1', options=[
                {'label': 'Dec 2021', 'value': '2021/12/1'},
                {'label': 'Mar 2022', 'value': '2022/03/1'},
                {'label': 'Jun 2022', 'value': '2022/06/1'},
                {'label': 'Sep 2022', 'value': '2022/09/1'}
            ]),
            ], style={'background-color': '#272838', 'float':'left', 'width': '25%', 'height': '50px'}),
        html.Label([
        "EIP1559 Scenarios",
        dcc.Dropdown(
            id='eip1559-dropdown', clearable=False,
            value='Disabled', options=[
                {'label': 'Disabled', 'value': 'Disabled'},
                {'label': 'Enabled: Steady State', 'value': 'Enabled: Steady State'},
                {'label': 'Enabled: MEV', 'value': 'Enabled: MEV'},
                {'label': 'Custom', 'value': 'Custom'},
            ]),
            html.Label([
            "EIP1559 Base Fee",
            dcc.Slider(
            id='eip1559-basefee-slider',
            min=0,
            max=100,
            step=5,
            marks={
                0: '0',
                25: '25',
                50: '50',
                75: '75',
                100: '100'
            },
            value=0,
            tooltip={'placement':'top'}
        )]),
            html.Label([
            "EIP1559 Validator Tips",
            dcc.Slider(
            id='eip1559-validator-tips-slider',
            min=0,
            max=100,
            step=5,
            marks={
                0: '0',
                25: '25',
                50: '50',
                75: '75',
                100: '100'
            },
            value=0,
            tooltip={'placement':'top'}
        )])
            ], style={'background-color': '#272838', 'float':'left', 'width': '25%', 'height': '90px'}),
        
        ],style={'background-color': '#272838', 'height': '200px'}),
        html.Div([
        dcc.Loading(
            id="loading-1",
            children=[dcc.Graph(id="graph")],
            type="default"
        )      
        ], style={"background-color": "#272838"}),
        ], style={"background-color": "#272838"})