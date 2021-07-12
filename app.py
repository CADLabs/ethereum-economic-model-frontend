# Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from utils import visualizations
import flask

# Plotly custom theme
import plotly.io as pio
from assets import plotly_theme
pio.templates.default = "cadlabs"

# Import layout components
from layout.layout import layout

# From notebook
#from utils import setup
import sys
import copy
import logging
import numpy as np
import pandas as pd
from datetime import datetime

import utils.visualizations as visualizations
from experiments.run import run
from model.types import Stage
from data.historical_values import df_ether_supply

# Import experiment templates
import experiments.templates.time_domain_analysis as time_domain_analysis


server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.LUX])
    
app.title = "Eth2 Calculator"
app.layout = layout

def run_simulation(validator_adoption, pos_launch_date, eip1559_basefee, eip1559_validator_tips):
    # Fetch the time-domain analysis experiment
    experiment = time_domain_analysis.experiment
    # Create a copy of the experiment simulation
    simulation = copy.deepcopy(experiment.simulations[0])
    simulation_0 = copy.deepcopy(simulation)
    simulation_0.model.params.update({
        'validator_process': [
            lambda _run, _timestep: float(validator_adoption),
        ],
        'date_pos': [
         datetime.strptime(pos_launch_date, "%Y/%m/%d")
        ],
        'eip1559_basefee_process': [
        lambda _run, _timestep: float(eip1559_basefee), 
    ],  # Gwei per gas
    'eip1559_tip_process': [
        lambda _run, _timestep: float(eip1559_validator_tips),
    ],  # Gwei per gas
    })

    df_0, _exceptions = run(simulation_0)
    return df_0, simulation_0.model.params

# Callbacks
@app.callback(
    Output('eip1559-basefee-slider', 'value'),
    Output('eip1559-validator-tips-slider', 'value'),
    [Input('eip1559-dropdown', 'value')]
)
def update_eip1559_sliders_by_scenarios(eip1559_dropdown):
    eip1559_scenarios = {'Disabled': [0, 0], 'Enabled: Steady State': [100, 1], 'Enabled: MEV':[70, 30]}
    if eip1559_dropdown == 'Custom':
        raise PreventUpdate
    return eip1559_scenarios[eip1559_dropdown][0], eip1559_scenarios[eip1559_dropdown][1]

@app.callback(
    Output('validator-adoption-slider', 'value'),
    [Input('validator-dropdown', 'value')]
)
def update_validator_adoption_sliders_by_scenarios(validator_dropdown):
    return validator_dropdown


# Define callback to update graph
@app.callback(
    Output('validator-dropdown', 'value'),
    Output('eip1559-dropdown', 'value'),
    Output('graph', 'figure'),

    Input("validator-adoption-slider", "value"),
     Input("pos-launch-date-dropdown", "value"),
     Input("eip1559-basefee-slider", "value"),
     Input("eip1559-validator-tips-slider", "value"),
)
def update_output_graph(validator_adoption,
                        pos_launch_date,
                        eip1559_basefee,
                        eip1559_validator_tips):
    df_0, parameters = run_simulation(validator_adoption, pos_launch_date, eip1559_basefee, eip1559_validator_tips)
    if validator_adoption not in [1.5, 3, 4.5]:
        validator_adoption = 'Custom'
    
    eip1559_fees = [eip1559_basefee, eip1559_validator_tips]
    if eip1559_fees in [[0, 0], [100, 1], [70, 30]]:
        if eip1559_fees == [0, 0]:
            eip1559 = 'Disabled'
        elif eip1559_fees == [100, 1]:
            eip1559 = 'Enabled: Steady State'
        else:
            eip1559 = 'Enabled: MEV'
    else:
        eip1559 = 'Custom'

    return (validator_adoption,
            eip1559,
            visualizations.plot_eth_supply_and_inflation_over_all_stages(df_ether_supply, df_0, parameters=parameters))

if __name__ == '__main__':
    app.run_server(debug=False)
