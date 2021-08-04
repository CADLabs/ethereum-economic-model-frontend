# Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import ClientsideFunction, Input, Output, State
from utils import visualizations
import flask

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

plots_validator_yields_file = open('./data/no_x_new_plots_validator_yields.json',)
fig_validator_yields = json.load(plots_validator_yields_file)

fig_cumulative_yields = json.load(open('./data/fig_cumulative_revenue_yields.json',))

simulation_data = data['data']['simulations']
historical_data = data['data']['historical']

# Configure scenarios
eip1559_scenarios = {'Disabled (Base Fee = 0)': 0, 'Enabled (Base Fee = 30)': 30}
validator_scenarios = {'Normal Adoption': 3, 'Low Adoption': 2, 'High Adoption': 4}
pos_dates_dropdown_scenarios = {'As planned (Dec 2021)': 0, 'Delayed 3 months (Mar 2022)': 1, 'Delayed 6 months (Jun 2022)': 2}

pos_dates_dropdown_poits = data['info']['parameters']['0']['points']

# define flask app.server
server = flask.Flask(__name__)

app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
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
                    },
                    {
                        'name': 'twitter:card',
                        'content': 'summary_large_image'
                    },
                    {
                        'name': 'twitter:site',
                        'content': '@CADLabs_org'
                    },
                    {
                        'name': 'twitter:title',
                        'content': 'Ethereum Economic Model Frontend'
                    },
                    {
                        'name': 'twitter:description',
                        'content': 'Ethereum is changing. This page illuminates potential ETH supply trajectories (ETH Supply Simulator) and yield implications for validators (Validator Yield Simulator).'
                    },
                    {
                        'name': 'twitter:image',
                        'content': 'https://user-images.githubusercontent.com/18421017/128188613-3afa2ab9-a857-416d-a8ab-7d625dbb2161.png'
                    }   
                    ])


app.title = "Ethereum Economic Model"
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
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_eip1559_priority_fee_slider_function'
    ),
    Output('eip1559-priority-fee-slider', 'value'),
    Input('eip1559-dropdown-2', 'value')
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_validator_adoption_slider_function'
    ),
    Output('validator-adoption-slider-2', 'value'),
    Input('validator-dropdown-2', 'value')
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_pos_date_slider_function'
    ),
    Output('pos-launch-date-slider-2', 'value'),
    Input('pos-launch-date-dropdown-2', 'value')
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_mev_slider_function'
    ),
    Output('mev-slider', 'value'),
    Input('mev-dropdown-2', 'value')
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
        mobile_figure,
    )

# Define callback to update graph
@app.callback(
    Output('validator-dropdown-2', 'value'),
    Output('pos-launch-date-dropdown-2', 'value'),
    Output('graph-yields', 'figure'),
    Input('validator-adoption-slider-2', 'value'),
    Input('pos-launch-date-slider-2', 'value'),
    Input('eip1559-priority-fee-slider', 'value'),
    Input('mev-slider', 'value')
)
def update_validator_yields_graph(validator_adoption,
                                  pos_launch_date_idx,
                                  priority_fee,
                                  mev):
    pos_launch_date = pos_dates_dropdown_poits[pos_launch_date_idx]
    mev_string = "{:.2f}".format(mev)
    if mev == 0:
        mev_string = '0.0'
    LookUp = str(pos_launch_date) + ':' + str(priority_fee) + ':' + mev_string + ':' + str(validator_adoption)
    validator_yields_data = fig_validator_yields[LookUp]

    for item in validator_yields_data:
        item.update({'x': fig_validator_yields['x']})

    validator_yields_figure = {
        'layout': fig_validator_yields['layout'],
        'data': validator_yields_data
    }

    _validator_scenarios = dict((v, k) for k, v in validator_scenarios.items())
    validator_dropdown = _validator_scenarios.get(validator_adoption, 'Custom Value')

    _pos_activation_scenarios = dict((v, k) for k, v in pos_dates_dropdown_scenarios.items())
    pos_activation_dropdown = _pos_activation_scenarios.get(pos_launch_date_idx, 'Custom Value')

    return (
        validator_dropdown,
        pos_activation_dropdown,
        validator_yields_figure
    )


if __name__ == '__main__':
    app.run_server(debug=False)
