# Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import ClientsideFunction, Input, Output, State
from utils import visualizations
import flask

# Additional dependencies
import json
import pandas as pd
from datetime import datetime

# Import layout components
from layout.layout import layout

# Import simulation data
with open('data/simulation_data.json') as json_file:
    data = json.load(json_file)

simulation_data = data['data']['simulations']
historical_data = data['data']['historical']

# define flask app.server
server = flask.Flask(__name__)

app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.LUX])
app.title = "Eth2 Calculator"
app.layout = layout


# Util functions
def load_simulation(validator_adoption, pos_launch_date, eip1559_basefee):
    simulation_data_lookup = (str(pos_launch_date).replace('/', '-').replace('-0', '-') +
                              ':' + str(eip1559_basefee) + ':' +
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
        'supply_inflation_pct': simulation_supply_inflation_pct,
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
    ClientsideFunction(
        namespace='clientside',
        function_name='update_eip1559_slider_function'
    ),
    Output('eip1559-basefee-slider', 'value'),
    Input('eip1559-dropdown', 'value')
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_validator_adoption_slider_function'
    ),
    Output('validator-adoption-slider', 'value'),
    Input('validator-dropdown', 'value')
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_eth_supply_chart_function'
    ),
    Output('graph', 'figure'),
    Output('validator-dropdown', 'value'),
    Output('eip1559-dropdown', 'value'),
    Input("eip1559-basefee-slider", "value"),
    Input("validator-adoption-slider", "value"),
    Input("pos-launch-date-dropdown", "value"),
    State('clientside-figure-store', 'data'),

)


if __name__ == '__main__':
    app.run_server(debug=False)
