# Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import ClientsideFunction, Input, Output, State
from utils import visualizations
import flask
from flask_talisman import Talisman

# Additional dependencies
import json
import copy
import pandas as pd
from datetime import datetime

# Import layout components
from layout.layout import layout

# Import simulation data
with open('data/simulation_data.json') as json_file:
    data = json.load(json_file)

plots_file = open('./data/plots_data.json',)
fig_data = json.load(plots_file)

simulation_data = data['data']['simulations']
historical_data = data['data']['historical']

# Configure scenarios
eip1559_scenarios = {'Disabled (Base Fee = 0)': 0, 'Enabled (Base Fee = 25)': 25}
validator_scenarios = {'Normal Adoption': 3, 'Low Adoption': 3 * 0.5, 'High Adoption': 3 * 1.5}
pos_dates_dropdown_scenarios = {'As planned (Dec 2021)': 0, 'Delayed 3 months (Mar 2022)': 1, 'Delayed 6 months (Jun 2022)': 2}

pos_dates_dropdown_poits = data['info']['parameters']['0']['points']

# define flask app.server
server = flask.Flask(__name__)
csp = {
    'default-src': '\'self\'',
    'script-src': ['\'self\'', '\'unsafe-inline\''],
}
Talisman(server, content_security_policy=csp)

app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                meta_tags=[
                    {
                        'name': 'viewport',
                        'content': 'width=device-width,initial-scale=1,minimum-scale=1,user-scalable=no'
                    },
                    {
                        'http-equiv': 'X-UA-Compatible',
                        'content': 'IE=edge,chrome=1',
                    },
                    {
                        'name': 'HandheldFriendly',
                        'content': 'true'
                    }])


app.title = "ETH Supply Simulator"
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
        function_name='update_pos_date_slider_function'
    ),
    Output('pos-launch-date-slider', 'value'),
    Input('pos-launch-date-dropdown', 'value')
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_validator_adoption_slider_function'
    ),
    Output('validator-adoption-slider', 'value'),
    Input('validator-dropdown', 'value')
)

"""
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_eth_supply_chart_function'
    ),
    Output('graph', 'figure'),
    Output('graph-mobile', 'figure'),
    Output('validator-dropdown', 'value'),
    Output('eip1559-dropdown', 'value'),
    Input("eip1559-basefee-slider", "value"),
    Input("validator-adoption-slider", "value"),
    Input("pos-launch-date-dropdown", "value"),
    State('clientside-figure-store', 'data'),
)
"""

# Define callback to update graph
@app.callback(
    Output('validator-dropdown', 'value'),
    Output('pos-launch-date-dropdown', 'value'),
    Output('eip1559-dropdown', 'value'),
    Output('graph', 'figure'),
    Output('graph-mobile', 'figure'),
    [Input('validator-adoption-slider', 'value'),
     Input('pos-launch-date-slider', 'value'),
     Input('eip1559-basefee-slider', 'value')]
)
def update_output_graph(validator_adoption, pos_launch_date_idx, eip1559_base_fee): 
    pos_launch_date = pos_dates_dropdown_poits[pos_launch_date_idx]
    LookUp = str(pos_launch_date) + ':' + str(eip1559_base_fee) + ':' + str(validator_adoption)
    HistoricalPlotData = fig_data["historical"]["data"]
    if (len(fig_data[LookUp]["data"]) < 6):
        fig_data[LookUp]["data"] = HistoricalPlotData + fig_data[LookUp]["data"]


    _validator_scenarios = dict((v, k) for k, v in validator_scenarios.items())
    validator_dropdown = _validator_scenarios.get(validator_adoption, 'Custom Value')

    _pos_activation_scenarios = dict((v, k) for k, v in pos_dates_dropdown_scenarios.items())
    pos_activation_dropdown = _pos_activation_scenarios.get(pos_launch_date_idx, 'Custom Value')

    _eip1559_scenarios = dict((v, k) for k, v in eip1559_scenarios.items())
    eip1559_dropdown = _eip1559_scenarios.get(eip1559_base_fee, 'Enabled (Custom Value)')

    
    mobile_figure = copy.deepcopy(fig_data[LookUp])
    mobile_figure["layout"]["annotations"].clear() 
    desktop_figure = fig_data[LookUp]
    
    return (
        validator_dropdown,
        pos_activation_dropdown,
        eip1559_dropdown,
        desktop_figure,
        mobile_figure
    )


if __name__ == '__main__':
    app.run_server(debug=False)
