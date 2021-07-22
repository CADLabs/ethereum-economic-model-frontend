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
pio.templates.default = "cadlabs_frontend"

# Import layout components
from layout.layout import layout

import pandas as pd
from datetime import datetime

# Import experiment templates

# Import simulation data
import json

with open('data/simulation_data.json') as json_file:
    data = json.load(json_file)

simulation_data = data['data']['simulations']
historical_data = data['data']['historical']

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.LUX])
    
app.title = "Eth2 Calculator"
app.layout = layout


# Util functions

def load_simulation(validator_adoption, pos_launch_date, eip1559_basefee):
    simulation_data_lookup = (str(pos_launch_date).replace('/', '-').replace('-0', '-') + ':' + 
                             str(eip1559_basefee) + ':' +
                             "{:.1f}".format(validator_adoption))

    historical_supply_inflation_pct = historical_data['supply_inflation_pct']
    historical_eth_supply = historical_data['eth_supply']
    historical_timestamp = historical_data['timestamp']

    simulation_supply_inflation_pct = simulation_data[simulation_data_lookup]['supply_inflation_pct']
    simulation_eth_supply = simulation_data[simulation_data_lookup]['eth_supply']
    simulation_timestamp = simulation_data['timestamp']

    data_historical = {
        'timestamp': historical_timestamp,
        'eth_supply': historical_eth_supply,
        'supply_inflation_pct': historical_supply_inflation_pct,
        'subset': 0
    }

    data_simulation = {
        'timestamp': simulation_timestamp,
        'eth_supply': simulation_eth_supply,
        'supply_inflation_pct':simulation_supply_inflation_pct,
        'subset': 0
    }

    df_historical_data = pd.DataFrame.from_dict(data_historical)
    df_historical_data['timestamp'] = pd.to_datetime(df_historical_data['timestamp'])

    df_simulation_data = pd.DataFrame.from_dict(data_simulation)
    df_simulation_data['timestamp'] = pd.to_datetime(df_simulation_data['timestamp'])

    parameters = {}
    parameters["date_eip1559"] = [datetime.strptime("2021/07/14", "%Y/%m/%d")]
    parameters["date_pos"] = [datetime.strptime(pos_launch_date, "%Y/%m/%d")]

    fig = visualizations.plot_eth_supply_and_inflation(df_historical_data,
                                                       df_simulation_data,
                                                       parameters=parameters)
    return fig


# Callbacks

app.clientside_callback(
    """
    function(EIP1559Dropdown) {
    EIP1559Scenarios = {'Disabled': 0, 'Enabled: Steady State': 100, 'Enabled: MEV':70};
    if (EIP1559Dropdown === 'Custom'){
        return window.dash_clientside.no_update
    }
    return EIP1559Scenarios[EIP1559Dropdown];
    }
    """,
    Output('eip1559-basefee-slider', 'value'),
    [Input('eip1559-dropdown', 'value')]
)


app.clientside_callback(
    """
    function(ValidatorDropdown) {
    ValidatorScenarios = {'Normal Adoption': 3, 'Low Adoption': 1.5, 'High Adoption':4.5};
    if (ValidatorDropdown === 'Custom'){
        return window.dash_clientside.no_update
    }
    return ValidatorScenarios[ValidatorDropdown];
    }
    """,
    Output('validator-adoption-slider', 'value'),
    [Input('validator-dropdown', 'value')]
)




# Define callback to update graph
app.clientside_callback(
    """
    function(EIP1559Slider, ValidatorAdoptionSlider, PosLaunchDate, FigurePlot) {
    const LookUp = PosLaunchDate + ':' + EIP1559Slider + ':' + ValidatorAdoptionSlider
    console.log(LookUp)
    if (EIP1559Slider === 0){
        return FigurePlot[0][LookUp]
    }
    return FigurePlot[0][LookUp];
    }
    """
 ,
    Output('graph', 'figure'),
    Input("eip1559-basefee-slider", "value"),
    Input("validator-adoption-slider", "value"),
    Input("pos-launch-date-dropdown", "value"),
    State('clientside-figure-store', 'data'),

)

"""
@app.callback(
    Output('validator-dropdown', 'value'),
    Output('eip1559-dropdown', 'value'),
    Output('graph', 'figure'),

    Input("validator-adoption-slider", "value"),
    Input("pos-launch-date-dropdown", "value"),
    Input("eip1559-basefee-slider", "value"),

    State('clientside-figure-store', 'data')
)
def update_output_graph(validator_adoption,
                        pos_launch_date,
                        eip1559_basefee,
                        clientside_figure_store):

    if validator_adoption == 3:
        validator_dropdown = 'Normal Adoption'
    elif validator_adoption == 1.5:
        validator_dropdown = 'Low Adoption'
    elif validator_adoption == 4.5:
        validator_dropdown = 'High Adoption'
    else:
        validator_dropdown = 'Custom'
    
    eip1559_basefee = int(eip1559_basefee)
    if int(eip1559_basefee) == 0:
        eip1559_dropdown = 'Disabled'
    elif int(eip1559_basefee) == 100:
        eip1559_dropdown = 'Enabled: Steady State'
    elif eip1559_basefee == 70:
        eip1559_dropdown = 'Enabled: MEV'
    else:
        eip1559_dropdown = 'Custom'

    fig = load_simulation(validator_adoption, pos_launch_date, eip1559_basefee)
    fig = clientside_figure_store[0]['1']


    return (validator_dropdown,
            eip1559_dropdown,
            fig)
"""

if __name__ == '__main__':
    app.run_server(debug=False)
