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


plots_file = open('./data/plots_data.json',)
fig_data = json.load(plots_file)

plots_validator_yields_file = open('./data/no_x_new_plots_validator_yields.json',)
fig_validator_yields = json.load(plots_validator_yields_file)


# Configure scenarios
eip1559_basefee_scenarios = {'Disabled (Base Fee = 0)': 0, 'Enabled (Base Fee = 30)': 30}
eip1559_priority_fee_scenarios = {'Disabled (Priority Fee = 0)': 0, 'Enabled (Priority Fee = 2)': 2}
validator_scenarios = {'Normal Adoption': 3, 'Low Adoption': 2, 'High Adoption': 4}
pos_dates_dropdown_scenarios = {'As planned (Dec 2021)': 0, 'Delayed 3 months (Mar 2022)': 1}
mev_scenarios = {'Disabled (MEV = 0)': 0, 'Enabled (MEV = 0.02)': 0.02}

pos_dates_dropdown_poits = [
                    "2021-12-1",
                    "2022-3-1",
                    "2022-6-1",
                    "2022-9-1",
                    "2022-12-1",
                    "2023-3-1",
                    "2023-6-1"
]

# define flask app.server
server = flask.Flask(__name__)
csp = {
    'default-src':['\'self\'', '\'unsafe-inline\''],
    'script-src': ['\'self\'', '\'unsafe-eval\'', '\'unsafe-inline\''],
    'style-src': ['\'self\'', '\'unsafe-inline\''],
    'img-src': ['\'self\'', '\'unsafe-eval\'', '\'unsafe-inline\'', 'data:'], 
}
#Talisman(server, content_security_policy=csp)

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
                        'content': 'https://user-images.githubusercontent.com/18421017/128346326-bfd67a8f-35bf-4a07-82fc-23e115dc3259.png'
                    }   
                    ])


app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-2XGCY6GEQJ"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-2XGCY6GEQJ');
            ga('send', 'pageview');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.title = "Ethereum Economic Model"
app.layout = layout


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

    _eip1559_basefee_scenarios = dict((v, k) for k, v in eip1559_basefee_scenarios.items())
    eip1559_dropdown = _eip1559_basefee_scenarios.get(eip1559_base_fee, 'Enabled (Custom Value)')

    
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
    Output('eip1559-dropdown-2', 'value'),
    Output('mev-dropdown-2', 'value'),
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
    if mev in [0, 0.10, 0.20, 0.30]:
        mev_string = "{:.1f}".format(mev)


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

    _eip1559_priority_fee_scenarios = dict((v, k) for k, v in eip1559_priority_fee_scenarios.items())
    eip1559_priority_fee_dropdown = _eip1559_priority_fee_scenarios.get(priority_fee, 'Enabled (Custom Value)')

    _pos_activation_scenarios = dict((v, k) for k, v in pos_dates_dropdown_scenarios.items())
    pos_activation_dropdown = _pos_activation_scenarios.get(pos_launch_date_idx, 'Custom Value')

    _mev_scenarios = dict((v, k) for k, v in mev_scenarios.items())
    mev_dropdown = _mev_scenarios.get(mev, 'Enabled (Custom Value)')

    return (
        validator_dropdown,
        pos_activation_dropdown,
        eip1559_priority_fee_dropdown,
        mev_dropdown,
        validator_yields_figure,   
    )


if __name__ == '__main__':
    app.run_server(debug=False)
