import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes


layout = html.Div([
    # Inputs
    html.Div([
        html.H1('Peak ETH Simulator'),
        # Validator Adoption
        html.Div([
            # Validator Adoption Dropdown
            html.Div([
                html.Label("Validator Adoption Scenario"),
                dcc.Dropdown(
                id='validator-dropdown',
                clearable=False,
                value=3,
                options=[
                    {'label': 'Normal Adoption', 'value': 3},
                    {'label': 'Low Adoption', 'value': 3 * 0.5},
                    {'label': 'High Adoption', 'value': 3 * 1.5},
                    {'label': 'Custom', 'value': 'Custom'}
                ] 
                )
            ]), 
            # Validator Adoption Slider
            html.Div([
                html.Label("New Validators per Epoch"),
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
                    tooltip={'placement': 'top'}
                )
            ])
            
        ], className='validator-section'),
        # Proof of Stake Activation Date Dropdown
        html.Div([
            html.Label("Proof-of-Stake Activation Date (\"The Merge\")"),
            dcc.Dropdown(
                id='pos-launch-date-dropdown',
                clearable=False,
                value='2021/12/1',
                options=[
                    {'label': 'Dec 2021', 'value': '2021/12/1'},
                    {'label': 'Mar 2022', 'value': '2022/03/1'},
                    {'label': 'Jun 2022', 'value': '2022/06/1'},
                    {'label': 'Sep 2022', 'value': '2022/09/1'}
                ]
            )
        ], className='pos-date-section'),
        # EIP1559
        html.Div([
            # EIP1559 Scenarios Dropdown
            html.Div([
                html.Label("EIP1559 Scenarios"),
                dcc.Dropdown(
                    id='eip1559-dropdown',
                    clearable=False,
                    value='Enabled: Steady State',
                    options=[
                        {'label': 'Disabled', 'value': 'Disabled'},
                        {'label': 'Enabled: Steady State', 'value': 'Enabled: Steady State'},
                        {'label': 'Enabled: MEV', 'value': 'Enabled: MEV'},
                        {'label': 'Custom', 'value': 'Custom'}
                    ]
                )
            ]),
            # Basefee slider
            html.Div([
                html.Label("Basefee (Gwei per gas)"),
                dcc.Slider(
                    id='eip1559-basefee-slider',
                    min=0,
                    max=100,
                    step=1,
                    marks={
                        0: '0',
                        25: '25',
                        50: '50',
                        75: '75',
                        100: '100'
                    },
                    value=100,
                    tooltip={'placement': 'top'},
                )
            ]),
            # Validator Tips Slider
            html.Div([
                html.Label("Average Priority Fee (Gwei per gas)"),
                dcc.Slider(
                    id='eip1559-validator-tips-slider',
                    min=0,
                    max=100,
                    step=1,
                    marks={
                        0: '0',
                        25: '25',
                        50: '50',
                        75: '75',
                        100: '100'
                    },
                    value=1,
                    tooltip={'placement': 'top'}
                )
            ])
        ], className='eip1559-section')
    ], className='input-row'),
    
    # Output
    html.Div([
        dcc.Loading(
            id='loading-1',
            children=[dcc.Graph(id='graph')],
            type='default'
        )
    ], className='output-row')
])
