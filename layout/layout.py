import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes

import json
from datetime import datetime

simulation_file = open('./data/simulation_data.json',)
simulation_data = json.load(simulation_file)

pos_dates_dropdown_poits = simulation_data['info']['parameters']['0']['points']
eip1559_slider_points = simulation_data['info']['parameters']['1']['points']
mid_eip1559_slider_point = eip1559_slider_points[len(eip1559_slider_points)//2]
validator_adoption_slider_points = simulation_data['info']['parameters']['2']['points']
mid_validator_adoption_slider_point = validator_adoption_slider_points[len(validator_adoption_slider_points)//2]


layout = html.Div([
    # Eth Supply Simulator Frame
    html.H1('Welcome to the ETH Supply Simulator!'),
    html.H2(['Ethereum’s monetary policy is changing. This simulator illuminates potential ETH supply trajectories. The underlying ', html.A('radCAD model', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ' is open-source.']),
    html.Div([
        # Inputs
        html.Div([
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
                        {'label': 'Custom Value', 'value': 'Custom Value'}
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
                            int(min(validator_adoption_slider_points)): str(int(min(validator_adoption_slider_points))),
                            mid_validator_adoption_slider_point: str(mid_validator_adoption_slider_point),
                            max(validator_adoption_slider_points): str(max(validator_adoption_slider_points)),
                        },
                        value=3,
                        tooltip={'placement': 'top'}
                    )
                ], className='slider-input')
                
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
                        value='Enabled (Base Fee = 25)',
                        options=[
                            {'label': 'Disabled (Base Fee = 0)', 'value': 'Disabled (Base Fee = 0)'},
                            {'label': 'Enabled (Base Fee = 25)', 'value': 'Enabled (Base Fee = 25)'},
                            {'label': 'Enabled (Custom Value)', 'value': 'Enabled (Custom Value)'}
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
                        value=25,
                        tooltip={'placement': 'top'},
                    )
                ], className='slider-input')
            ], className='eip1559-section')
        ], className='input-row'),
        
        # Output
        html.Div([
            dcc.Graph(id='graph-mobile', className='output-graph-mobile'),
            dcc.Graph(id='graph', className='output-graph')
        ], className='output-row')
    ], className='simulator-frame'),
    html.Div([
        html.P(['This ', html.A('radCAD', href='https://github.com/CADLabs/radCAD', target='_blank'), ' front-end is based on version 1.0.0 of the ', html.A('open-source CADLabs Ethereum Economic Model', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ', which had been created in collaboration with the Ethereum Robust Incentives Group (RIG), supported by an ', html.A('Ethereum ESP', href='https://esp.ethereum.foundation/en/', target='_blank'),' grant. Please refer to the ', html.A('Github repo', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ' for context and assumptions of the model. To suggest improvements of any kind, either submit PRs directly, leave us your ideas/comments/doubts/praise in this ', html.A('feedback form', href='https://docs.google.com/forms/d/1LNhCFJ4-Jj7wg6bQJG1UGuP69zMU97L-g38nobTJs8I/viewform?edit_requested=true', target='_blank'), ', or drop us a note at ', html.A('contact@cadlabs.org', href='mailto:contact@cadlabs.org'), '.'])
    ], className='chart-footer'),
    html.Footer([
        html.P('Powered by:'),
        html.A(
            html.Img(src='assets/radcad-logo.svg', height='60px'),
            href='https://github.com/CADLabs/radCAD',
            target='_blank'
        ),
        html.P('Created by:'),
        html.A(
            html.Img(src='assets/cadlabs-logo.svg', height='60px'),
            href='https://twitter.com/CADLabs_org',
            target='_blank'
        )
        
    ])
])
