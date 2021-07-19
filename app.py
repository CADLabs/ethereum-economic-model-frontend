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

# From notebook
#from utils import setup
import pandas as pd

import utils.visualizations as visualizations

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

    data_historical = {
        'timestamp': historical_timestamp,
        'eth_supply': historical_eth_supply,
        'supply_inflation_pct': historical_supply_inflation_pct,
        'subset': 0
    }

    simulation_supply_inflation_pct = simulation_data[simulation_data_lookup]['supply_inflation_pct']
    simulation_eth_supply = simulation_data[simulation_data_lookup]['eth_supply']
    simulation_timestamp = simulation_data['timestamp']

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

    fig = visualizations.plot_eth_supply_and_inflation_over_all_stages(df_historical_data, df_simulation_data)
    return fig


# Callbacks

app.clientside_callback(
    """
    function(EIP1559Dropdown) {
    EIP1559Scenarios = {'Disabled': 0, 'Enabled: Steady State': 90, 'Enabled: MEV':70};
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
@app.callback(
    Output('validator-dropdown', 'value'),
    Output('eip1559-dropdown', 'value'),
    Output('graph', 'figure'),

    Input("validator-adoption-slider", "value"),
     Input("pos-launch-date-dropdown", "value"),
     Input("eip1559-basefee-slider", "value"),
)
def update_output_graph(validator_adoption,
                        pos_launch_date,
                        eip1559_basefee):

    if validator_adoption == 3:
        validator_dropdown = 'Normal Adoption'
    elif validator_adoption == 1.5:
        validator_dropdown = 'Low Adoption'
    elif validator_adoption == 4.5:
        validator_dropdown = 'High Adoption'
    else:
        validator_dropdown = 'Custom'
    
    eip1559_fees = eip1559_basefee
    if eip1559_fees == 0:
        eip1559 = 'Disabled'
    elif eip1559_fees == 90:
        eip1559 = 'Enabled: Steady State'
    elif eip1559_fees == 70:
        eip1559 = 'Enabled: MEV'
    else:
        eip1559 = 'Custom'

    fig = load_simulation(validator_adoption, pos_launch_date, eip1559_basefee)

    return (validator_dropdown,
            eip1559,
            fig)

if __name__ == '__main__':
    app.run_server(debug=False)
