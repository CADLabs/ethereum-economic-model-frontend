import dash_html_components as html
import dash_bootstrap_components as dbc


exogenous_processes = html.Div(
    [
        html.H3('Exogenous Processes', style={"color": "white"}),
        html.Hr(className="under-title"),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="eth_price", type="number", placeholder=" "),
                dbc.Label("Eth price (USD)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="eth_staked", type="number", placeholder=" "),
                dbc.Label("Eth Staked")], className="input-label-float")]),

                dbc.Col([
                dbc.Button("Open eth2 specs",
                            id="collapse-button-eth2",
                            className="button")]),

                dbc.Col([
                dbc.Button("Open validator specs",
                            id="collapse-button-validator",
                            className="button")]),

                dbc.Col([
                dbc.Button("Run simulation",
                            id="button-run-simulation",
                            className="button")])
            ], justify="start"
        ),
    ]
)