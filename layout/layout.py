import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes


layout = html.Div([
    # Inputs
    html.Div([
        html.H1('ETH Supply Simulator'),
        # Validator Adoption
        html.Div([
            # Validator Adoption Dropdown
            html.Div([
                html.Label("Validator Adoption Scenario"),
                dcc.Dropdown(
                id='validator-dropdown',
                clearable=False,
                value='Normal Adoption',
                options=[
                    {'label': 'Normal Adoption', 'value': 'Normal Adoption'},
                    {'label': 'Low Adoption', 'value': 'Low Adoption'},
                    {'label': 'High Adoption', 'value': 'High Adoption'},
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
                    max=7.5,
                    step=0.5,
                    marks={
                        0: '0',
                        4: '5',
                        7.5: '7.5',
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
                html.Label("EIP1559 Scenario"),
                dcc.Dropdown(
                    id='eip1559-dropdown',
                    clearable=False,
                    value='Enabled: Steady State',
                    options=[
                        {'label': 'Disabled (Base Fee 0, Priority Fee 0)', 'value': 'Disabled'},
                        {'label': 'Enabled / No MEV (Base Fee 100, Priority Fee 1)', 'value': 'Enabled: Steady State'},
                        {'label': 'Enabled / MEV (Base Fee 70, Priority Fee 30)', 'value': 'Enabled: MEV'},
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
                    step=10,
                    marks={
                        0: '0',
                        50: '50',
                        100: '100'
                    },
                    value=90,
                    tooltip={'placement': 'top'},
                )
            ])
        ], className='eip1559-section')
    ], className='input-row'),
    
    # Output
    html.Div([
        dcc.Graph(id='graph', className='output-graph')
    ], className='output-row')
])
