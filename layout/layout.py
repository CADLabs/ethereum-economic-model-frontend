import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components.H2 import H2
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
    html.H1('Welcome to ethmodel.io!'),
    html.H2(['Ethereum is changing. This page illuminates potential ETH supply trajectories (ETH Supply Simulator) and yield implications for validators (Validator Yield Simulator). The underlying ', html.A('cadCAD/radCAD model', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ' is open-source, assumptions are summarized ', html.A('here', href='https://github.com/CADLabs/ethereum-economic-model/blob/main/ASSUMPTIONS.md', target='_blank'), '. Repo contributions and ', html.A('feedback', href='https://docs.google.com/forms/d/1LNhCFJ4-Jj7wg6bQJG1UGuP69zMU97L-g38nobTJs8I/viewform?edit_requested=true', target='_blank'), ' are most welcome. For a comprehensive intro to running, modifying and extending the model, consider the upcoming ', html.A('cadCAD Masterclass', href='https://www.cadcad.education/course/masterclass-ethereum', target='_blank'), ' (free). If you enjoy using this website, consider ', html.A('sharing', href='https://twitter.com/intent/tweet?text=Check%20out%20ethmodel.io,%20an%20Ethereum%20protocol%20simulation%20web%20frontend%20of%20the%20open-source%20@cadCAD_org%20model%20available%20at&url=https://bit.ly/3jnuISh.', target='_blank'), ' it, so more people benefit.']),
    html.Div([
        html.Div([
            html.H3('ETH Supply Simulator'),
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
                            {'label': 'Normal Adoption (Historical Average)', 'value': 'Normal Adoption'},
                            {'label': 'Low Adoption (50% Slower)', 'value': 'Low Adoption'},
                            {'label': 'High Adoption (50% Faster)', 'value': 'High Adoption'},
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
                    html.Div([
                    html.Label("Proof-of-Stake Activation Scenario"),
                    dcc.Dropdown(
                        id='pos-launch-date-dropdown',
                        clearable=False,
                        value='As planned (Dec 2021)',
                        options=[
                            {'label': 'As planned (Dec 2021)', 'value': 'As planned (Dec 2021)'},
                            {'label': 'Delayed 3 months (Mar 2022)', 'value': 'Delayed 3 months (Mar 2022)'},
                            {'label': 'Delayed 6 months (Jun 2022)', 'value': 'Delayed 6 months (Jun 2022)'},
                            {'label': 'Custom Value', 'value': 'Custom Value'}   
                        ])
                    ]),
                    html.Div([
                        html.Label("Activation Date"),
                        dcc.Slider(
                            id='pos-launch-date-slider',
                            min=0,
                            max=len(pos_dates_dropdown_poits)-1,
                            step=1,
                            marks={
                            idx: datetime.strptime(date, '%Y-%m-%d').strftime('%y-%m') for idx, date in enumerate(pos_dates_dropdown_poits)
                            },
                            value=0,
                        )
                    ], className='slider-input')

                ], className='pos-date-section'),
                
                # EIP1559
                html.Div([
                    # EIP1559 Scenarios Dropdown
                    html.Div([
                        html.Label("EIP-1559 Base Fee Scenario"),
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
                        html.Label("Base Fee (Gwei per gas)"),
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
            ], className='output-row'),
        ], className='simulator-frame'),
        html.Div([
            html.H3('Validator Yield Simulator'),
            html.Div([
                # Validator Adoption
                html.Div([
                    # Validator Adoption Dropdown
                    html.Div([
                        html.Label("Validator Adoption Scenario"),
                        dcc.Dropdown(
                        id='validator-dropdown-2',
                        clearable=False,
                        value='Normal Adoption',
                        options=[
                            {'label': 'Normal Adoption (Historical Average)', 'value': 'Normal Adoption'},
                            {'label': 'Low Adoption (50% Slower)', 'value': 'Low Adoption'},
                            {'label': 'High Adoption (50% Faster)', 'value': 'High Adoption'},
                            {'label': 'Custom Value', 'value': 'Custom Value'}
                        ] 
                        )
                    ]), 
                    # Validator Adoption Slider
                    html.Div([
                        html.Label("New Validators per Epoch"),
                        dcc.Slider(
                            id='validator-adoption-slider-2',
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
                    html.Div([
                    html.Label("Proof-of-Stake Activation Scenario"),
                    dcc.Dropdown(
                        id='pos-launch-date-dropdown-2',
                        clearable=False,
                        value='As planned (Dec 2021)',
                        options=[
                            {'label': 'As planned (Dec 2021)', 'value': 'As planned (Dec 2021)'},
                            {'label': 'Delayed 3 months (Mar 2022)', 'value': 'Delayed 3 months (Mar 2022)'},
                            {'label': 'Delayed 6 months (Jun 2022)', 'value': 'Delayed 6 months (Jun 2022)'},
                            {'label': 'Custom Value', 'value': 'Custom Value'}   
                        ])
                    ]),
                    html.Div([
                        html.Label("Activation Date"),
                        dcc.Slider(
                            id='pos-launch-date-slider-2',
                            min=0,
                            max=len(pos_dates_dropdown_poits)-1,
                            step=1,
                            marks={
                            idx: datetime.strptime(date, '%Y-%m-%d').strftime('%y-%m') for idx, date in enumerate(pos_dates_dropdown_poits)
                            },
                            value=0,
                        )
                    ], className='slider-input')

                ], className='pos-date-section'),
                
                # EIP1559
                html.Div([
                    # EIP1559 Scenarios Dropdown
                    html.Div([
                        html.Label("EIP-1559 Scenario"),
                        dcc.Dropdown(
                            id='eip1559-dropdown-2',
                            clearable=False,
                            value='Enabled (Priority Fee = 2)',
                            options=[
                                {'label': 'Disabled (Priority Fee = 0)', 'value': 'Disabled (Priority Fee = 0)'},
                                {'label': 'Enabled (Priority Fee = 2)', 'value': 'Enabled (Priority Fee = 2)'},
                                {'label': 'Enabled (Custom Value)', 'value': 'Enabled (Custom Value)'}
                            ]
                        )
                    ]),
                    # Basefee slider
                    html.Div([
                        html.Label("Priority Fee (Gwei per gas)"),
                        dcc.Slider(
                            id='eip1559-priority-fee-slider',
                            min=0,
                            max=20,
                            step=2,
                            marks={
                                0: str(0),
                                10: str(10),
                                20: str(20)
                            },
                            value=2,
                            tooltip={'placement': 'top'},
                        )
                    ], className='slider-input')
                ], className='eip1559-section'),
                # MEV
                html.Div([
                    # MEV Scenarios Dropdown
                    html.Div([
                        html.Label("MEV Scenario"),
                        dcc.Dropdown(
                            id='mev-dropdown-2',
                            clearable=False,
                            value='Enabled (MEV = 0.0115)',
                            options=[
                                {'label': 'Disabled (MEV = 0)', 'value': 'Disabled (MEV = 0)'},
                                {'label': 'Enabled (MEV = 0.0115)', 'value': 'Enabled (MEV = 0.0115)'},
                                {'label': 'Enabled (Custom Value)', 'value': 'Enabled (Custom Value)'}
                            ]
                        )
                    ]),
                    # Basefee slider
                    html.Div([
                        html.Label("MEV (ETH per block)"),
                        dcc.Slider(
                            id='mev-slider',
                            min=0,
                            max=0.115,
                            step=0.0115,
                            marks={
                                0: str(0),
                                0.0575: str(0.0575),
                                0.115: str(0.115)
                            },
                            value=0.0115,
                            tooltip={'placement': 'top'},
                        )
                    ], className='slider-input')
                ], className='eip1559-section')
            ], className='input-row-2'),
            # Output
            html.Div([
                dcc.Graph(id='graph-yields', className='output-graph-2')
            ], className='output-row-2')
        ], className='simulator-frame'),
        html.Div([
            html.P(['This ', html.A('radCAD', href='https://github.com/CADLabs/radCAD', target='_blank'), ' front-end is based on version 1.1.0 of the ', html.A('open-source CADLabs Ethereum Economic Model', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ', which had been created in collaboration with the Ethereum Robust Incentives Group (RIG), supported by an ', html.A('Ethereum ESP', href='https://esp.ethereum.foundation/en/', target='_blank'),' grant. Please refer to the ', html.A('Github repo', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ' for further context. To suggest improvements of any kind, either submit PRs directly, leave us your ideas/comments/doubts/praise in this ', html.A('feedback form', href='https://docs.google.com/forms/d/1LNhCFJ4-Jj7wg6bQJG1UGuP69zMU97L-g38nobTJs8I/viewform?edit_requested=true', target='_blank'), '. For researchers actively using the model or planning its use for a concrete project, we are running a small private channel (drop us a note at ', html.A('contact@cadlabs.org', href='mailto: contact@cadlabs.org', target='_blank'), ' and introduce your project).'])
        ], className='chart-footer'),
    ], className='output-container'),
    html.Footer([
        html.P('Powered by:'),
        html.A(
            html.Img(src='assets/radcad-logo.svg', height='60px'),
            href='https://github.com/CADLabs/radCAD',
            target='_blank'
        ),
        html.P('Created by:'),
        html.A(
            html.Img(src='assets/cadlabs-logo.svg', height='50px'),
            href='https://twitter.com/CADLabs_org',
            target='_blank'
        )
        
    ])
])
