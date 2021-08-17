import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json

simulation_file = open('./data/simulation_data.json',)
simulation_data = json.load(simulation_file)
pos_dates_dropdown_poits = simulation_data['info']['parameters']['0']['points']
eip1559_slider_points = simulation_data['info']['parameters']['1']['points']
mid_eip1559_slider_point = eip1559_slider_points[len(eip1559_slider_points)//2]
validator_adoption_slider_points = simulation_data['info']['parameters']['2']['points']
mid_validator_adoption_slider_point = validator_adoption_slider_points[len(validator_adoption_slider_points)//2]



def get_max_validator_cap_layout(id_dict, className):
    max_validator_cap_layout = html.Div(
        [
            # Max Validator Cap Dropdown
            html.Div(
                [
                    html.Label("Validator Cap Scenario"),
                    dcc.Dropdown(
                        id=id_dict['dropdown'],
                        clearable=False,
                        value='No Validator Cap',
                        options=[
                            {'label': 'No Validator Cap', 'value': 'No Validator Cap'},
                            {'label': "Vitalik's Proposal (max 524K validators)", 'value': "Vitalik's Proposal (max 524K validators)"},
                            {'label': 'Custom Value', 'value': 'Custom Value'}
                        ] 
                    )
                ]
            ), 
            # Max Validator Cap Slider
            html.Div(
                [
                    html.Label("Max Validator Cap (N° of Awake Validators)"),
                    dcc.Slider(
                        id=id_dict['slider'],
                        min=0,
                        max=1048,
                        step=524,
                        marks={
                            0: 'Disabled',
                            524: '524K',
                            1048: '1048K',
                        },
                        value=0,
                    )
                ], className='slider-input'
            )
            
        ], className=className
    )
    return max_validator_cap_layout


def get_validator_adoption_layout(id_dict, className):
    validator_adoption_layout = html.Div(
        [
            # Validator Adoption Dropdown
            html.Div(
                [
                    html.Label("Validator Adoption Scenario"),
                    dcc.Dropdown(
                        id=id_dict['dropdown'],
                        clearable=False,
                        value='Normal Adoption',
                        options=[
                            {'label': 'Normal Adoption (Historical Average)', 'value': 'Normal Adoption'},
                            {'label': 'Low Adoption (50% Slower)', 'value': 'Low Adoption'},
                            {'label': 'High Adoption (50% Faster)', 'value': 'High Adoption'},
                            {'label': 'Custom Value', 'value': 'Custom Value'}
                        ]
                    )
                ]
            ), 
            # Validator Adoption Slider
            html.Div([
                html.Label("New Validators per Epoch"),
                dcc.Slider(
                    id=id_dict['slider'],
                    min=0,
                    max=6,
                    step=1,
                    marks={
                        0: '0',
                        1: '1',
                        2: '2',
                        3: '3',
                        4: '4',
                        5: '5',
                        6: '6',
                    },
                    value=3,
                    tooltip={'placement': 'top'}
                )
            ], className='slider-input')
        ], className=className
    )
    return validator_adoption_layout


def get_pos_launch_date_layout(id_dict, className):
    pos_launch_date_layout = html.Div(
        [
            html.Div(
                [
                    html.Label("Proof-of-Stake Activation Scenario"),
                    dcc.Dropdown(
                        id=id_dict['dropdown'],
                        clearable=False,
                        value='Delayed 3 months (Mar 2022)',
                        options=[
                            {'label': 'Optimistic (Dec 2021)', 'value': 'As planned (Dec 2021)'},
                            {'label': 'Community Consensus (Mar 2022)', 'value': 'Delayed 3 months (Mar 2022)'},
                            {'label': 'Real soon™ (Custom Value)', 'value': 'Custom Value'}
                        ])
                ]
            ),
            html.Div(
                [
                    html.Label("Activation Date"),
                    dcc.Slider(
                        id=id_dict['slider'],
                        min=0,
                        max=len(pos_dates_dropdown_poits)-1,
                        step=1,
                        marks={
                        idx: datetime.strptime(date, '%Y-%m-%d').strftime('%y-%m') for idx, date in enumerate(pos_dates_dropdown_poits)
                        },
                        value=1,
                    )
                ], className='slider-input'
            )

        ], className=className
    )
    return pos_launch_date_layout


def get_eip1559_base_fee_layout(id_dict, className):
    eip1559_base_fee_layout = html.Div(
        [
            # EIP1559 Scenarios Dropdown
            html.Div(
                [
                    html.Label("EIP-1559 Base Fee Scenario"),
                    dcc.Dropdown(
                        id=id_dict['dropdown'],
                        clearable=False,
                        value='Enabled (Base Fee = 0)',
                        options=[
                            {'label': 'Disabled (Base Fee = 0)', 'value': 'Disabled (Base Fee = 0)'},
                            {'label': 'Enabled (Base Fee = 30)', 'value': 'Enabled (Base Fee = 30)'},
                            {'label': 'Enabled (Custom Value)', 'value': 'Enabled (Custom Value)'}
                        ]
                    )
                ]
            ),
            # Basefee slider
            html.Div(
                [
                    html.Label("Base Fee (Gwei per gas)"),
                    dcc.Slider(
                        id=id_dict['slider'],
                        min=min(eip1559_slider_points),
                        max=max(eip1559_slider_points),
                        step=eip1559_slider_points[1] - eip1559_slider_points[0],
                        marks={
                            0: '0',
                            25: '25',
                            50: '50',
                            75: '75',
                            100: '100'
                        },
                        value=30,
                        tooltip={'placement': 'top'},
                    )
                ], className='slider-input'
            )
        ], className=className
    )
    return eip1559_base_fee_layout


def get_eip1559_priority_fee_layout(id_dict, className):
    eip1559_priority_fee_layout = html.Div(
        [
            # EIP1559 Scenarios Dropdown
            html.Div(
                [
                    html.Label("EIP-1559 Priority Fee Scenario"),
                    dcc.Dropdown(
                        id=id_dict['dropdown'],
                        clearable=False,
                        value='Enabled (Priority Fee = 2)',
                        options=[
                            {'label': 'Disabled (Priority Fee = 0)', 'value': 'Disabled (Priority Fee = 0)'},
                            {'label': 'Enabled (Priority Fee = 2)', 'value': 'Enabled (Priority Fee = 2)'},
                            {'label': 'Enabled (Custom Value)', 'value': 'Enabled (Custom Value)'}
                        ]
                    )
                ]
            ),
            # Basefee slider
            html.Div(
                [
                    html.Label("Priority Fee (Gwei per gas)"),
                    dcc.Slider(
                        id=id_dict['slider'],
                        min=0,
                        max=20,
                        step=2,
                        marks={
                            0: '0',
                            4: '5',
                            8: '8',
                            12: '12',
                            16: '16',
                            20: '20'
                        },
                        value=2,
                        tooltip={'placement': 'top'},
                    )
                ], className='slider-input'
            )
        ], className=className
    )
    return eip1559_priority_fee_layout


def get_mev_layout(id_dict, className):
    mev_layout = html.Div(
        [
            # MEV Scenarios Dropdown
            html.Div(
                [
                    html.Label("MEV Scenario"),
                    dcc.Dropdown(
                        id=id_dict['dropdown'],
                        clearable=False,
                        value='Enabled (MEV = 0.02)',
                        options=[
                            {'label': 'Disabled (MEV = 0)', 'value': 'Disabled (MEV = 0)'},
                            {'label': 'Enabled (MEV = 0.02)', 'value': 'Enabled (MEV = 0.02)'},
                            {'label': 'Enabled (Custom Value)', 'value': 'Enabled (Custom Value)'}
                        ]
                    )
                ]
            ),
            # Basefee slider
            html.Div(
                [
                    html.Label("MEV (ETH per block)"),
                    dcc.Slider(
                        id=id_dict['slider'],
                        min=0,
                        max=0.30,
                        step=0.02,
                        marks={
                            0: str(0),
                            0.10: '0.10',
                            0.20: '0.20',
                            0.30: '0.30'
                        },
                        value=0.02,
                        tooltip={'placement': 'top'},
                    )
                ], className='slider-input'
            )
        ], className=className
    )
    return mev_layout
