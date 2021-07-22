import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes

import json
from datetime import datetime
  
# Opening JSON file
plots_file = open('./data/plots_data.json',)
fig_data = json.load(plots_file)

simulation_file = open('./data/simulation_data.json',)
simulation_data = json.load(simulation_file)

pos_dates_dropdown_poits = simulation_data['info']['parameters']['0']['points']
eip1559_slider_points = simulation_data['info']['parameters']['1']['points']
mid_eip1559_slider_point = eip1559_slider_points[len(eip1559_slider_points)//2]
validator_adoption_slider_points = simulation_data['info']['parameters']['2']['points']
mid_validator_adoption_slider_point = validator_adoption_slider_points[len(validator_adoption_slider_points)//2]


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
                    min=min(validator_adoption_slider_points),
                    max=max(validator_adoption_slider_points),
                    step=validator_adoption_slider_points[1] - validator_adoption_slider_points[0],
                    marks={
                        min(validator_adoption_slider_points): str(min(validator_adoption_slider_points)),
                        mid_validator_adoption_slider_point: str(mid_validator_adoption_slider_point),
                        max(validator_adoption_slider_points): str(max(validator_adoption_slider_points)),
                    },
                    value=mid_validator_adoption_slider_point,
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
                value=pos_dates_dropdown_poits[0],
                options=[
                    {'label': datetime.strptime(date, '%Y-%m-%d').strftime('%B, %Y'), 'value': date} for date in pos_dates_dropdown_poits
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
                    min=min(eip1559_slider_points),
                    max=max(eip1559_slider_points),
                    step=eip1559_slider_points[1] - eip1559_slider_points[0],
                    marks={
                        min(eip1559_slider_points): str(min(eip1559_slider_points)),
                        mid_eip1559_slider_point: str(mid_eip1559_slider_point),
                        max(eip1559_slider_points): str(max(eip1559_slider_points))
                    },
                    value=max(eip1559_slider_points),
                    tooltip={'placement': 'top'},
                )
            ])
        ], className='eip1559-section')
    ], className='input-row'),
    
    # Output
    html.Div([
        dcc.Graph(id='graph', className='output-graph'),
        dcc.Store(
        id='clientside-figure-store',
        data=[fig_data]
    ),
    ], className='output-row')
])
