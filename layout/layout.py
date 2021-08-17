import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components.H2 import H2
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes
from layout.inputs.inputs_layout import (get_max_validator_cap_layout,
                                         get_validator_adoption_layout,
                                         get_pos_launch_date_layout,
                                         get_eip1559_base_fee_layout,
                                         get_eip1559_priority_fee_layout,
                                         get_mev_layout)

import copy
import json
import compress_json
from datetime import datetime

simulation_file = open('./data/simulation_data.json',)
simulation_data = json.load(simulation_file)

#plots_file = open('./data/plots_data_new.json',)
fig_data = compress_json.load('./data/plots_data_new.json.gz')

#plots_validator_yields_file = open('./data/no_x_new_plots_validator_yields.json',)
fig_validator_yields = compress_json.load('./data/plots_validator_yields.json.gz')


initial_fig_eth_supply = fig_data['2021-12-1:0:0:None']
#{
#    'layout':fig_data['2021-12-1:0:0:None']["layout"],
#    'data': fig_data["historical"]["data"] + fig_data['2021-12-1:0:0:None']["data"]
#}
initial_fig_eth_supply_mobile = copy.deepcopy(initial_fig_eth_supply)
initial_fig_eth_supply_mobile["layout"]["annotations"].clear() 

initial_fig_validator_yields =  fig_validator_yields['2022-3-1:2:0.02:3:None']
#{
#        'layout': fig_validator_yields['layout'],
#        'data': fig_validator_yields['2022-3-1:2:0.02:3']
#    }


eth_supply_simulator_layout = html.Div(
    [
        html.H3('ETH Supply Simulator'),
        # Inputs
        html.Div(
            [
                # Max Validator Cap
                get_max_validator_cap_layout(
                    {
                        'dropdown': 'max-validator-cap-dropdown',
                        'slider': 'max-validator-cap-slider'
                    },
                    className='max-validator-cap-section'
                ),
                # Validator Adoption
                get_validator_adoption_layout(
                    {
                        'dropdown': 'validator-dropdown',
                        'slider': 'validator-adoption-slider'
                    },
                    className='validator-section'
                ),
                # Proof of Stake Activation Date
                get_pos_launch_date_layout(
                    {
                        'dropdown': 'pos-launch-date-dropdown',
                        'slider': 'pos-launch-date-slider'
                    },
                    className='pos-date-section'
                ),
                # EIP1559 Base Fee
                get_eip1559_base_fee_layout(
                    {
                        'dropdown': 'eip1559-dropdown',
                        'slider': 'eip1559-basefee-slider'
                    },
                    className='eip1559-section'
                )
            ], className='input-row'
        ),
        # Output
        html.Div(
            [
                dcc.Graph(id='graph-mobile', className='output-graph-mobile', figure=initial_fig_eth_supply_mobile),
                dcc.Graph(id='graph', className='output-graph', figure=initial_fig_eth_supply)
            ], className='output-row'
        ),
    ], className='simulator-frame'
)

validator_yield_simulator_layout = html.Div(
    [
        html.H3('Validator Yield Simulator'),
        html.Div(
            [
                # Max Validator Cap
                get_max_validator_cap_layout(
                    {
                        'dropdown': 'max-validator-cap-dropdown-2',
                        'slider': 'max-validator-cap-slider-2'
                    },
                    className='max-validator-cap-section-2'
                ),
                # Validator Adoption
                get_validator_adoption_layout(
                    {
                        'dropdown': 'validator-dropdown-2',
                        'slider': 'validator-adoption-slider-2'
                    },
                    className='validator-adoption-section-2'
                ),
                # Proof of Stake Activation Date
                get_pos_launch_date_layout(
                    {
                        'dropdown': 'pos-launch-date-dropdown-2',
                        'slider': 'pos-launch-date-slider-2'
                    },
                    className='pos-date-section-2'
                ),
                # EIP1559
                get_eip1559_priority_fee_layout(
                    {
                        'dropdown': 'eip1559-dropdown-2',
                        'slider': 'eip1559-priority-fee-slider'
                    },
                    className='eip1559-section-2'
                ),
                # MEV
                
                get_mev_layout(
                    {
                        'dropdown': 'mev-dropdown-2',
                        'slider': 'mev-slider'
                    },
                    className='mev-section-2'
                ),
            ], className='input-row-2'),
        # Output
        html.Div([
            dcc.Graph(id='graph-yields', className='output-graph-2', figure=initial_fig_validator_yields)
        ], className='output-row-2')
    ], className='simulator-frame'
)

layout = html.Div([
    # Eth Supply Simulator Frame
    html.H1('Welcome to ethmodel.io!'),
    html.H2(['Ethereum is changing. This page illuminates potential ETH supply trajectories (ETH Supply Simulator) and yield implications for validators (Validator Yield Simulator). The underlying ', html.A('cadCAD/radCAD model', href='https://github.com/CADLabs/ethereum-economic-model', target='_blank'), ' is open-source, assumptions are summarized ', html.A('here', href='https://github.com/CADLabs/ethereum-economic-model/blob/main/ASSUMPTIONS.md', target='_blank'), '. Repo contributions and ', html.A('feedback', href='https://docs.google.com/forms/d/1LNhCFJ4-Jj7wg6bQJG1UGuP69zMU97L-g38nobTJs8I/viewform?edit_requested=true', target='_blank'), ' are most welcome. For a comprehensive intro to running, modifying and extending the model, consider the upcoming ', html.A('cadCAD Masterclass', href='https://www.cadcad.education/course/masterclass-ethereum', target='_blank'), ' (free). If you enjoy using this website, consider ', html.A('sharing', href='https://twitter.com/intent/tweet?&text=Check%20out%20ethmodel.io,%20an%20Ethereum%20protocol%20simulation%20frontend%20of%20the%20open-source%20@cadCAD_org%20model%20available%20at&url=https://bit.ly/3jnuISh.', target='_blank'), ' it, so more people benefit.']),
    eth_supply_simulator_layout,
    validator_yield_simulator_layout,
    html.Div([
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
