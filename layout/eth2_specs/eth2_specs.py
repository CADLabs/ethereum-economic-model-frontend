import dash_html_components as html
import dash_bootstrap_components as dbc


eth2_specs = html.Div(
    [
        dbc.Collapse([
        html.Hr(),
        html.H3('Eth2 Specs', style={"color": "white"}),
        html.Hr(className="under-title"),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="BASE_REWARD_FACTOR", type="number", placeholder=" "),
                dbc.Label("Base reward factor")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="BASE_REWARDS_PER_EPOCH", type="number", placeholder=" "),
                dbc.Label("Base rewards per epoch")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="MAX_EFFECTIVE_BALANCE", type="number", placeholder=" "),
                dbc.Label("Max effective balance (ETH)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="EFFECTIVE_BALANCE_INCREMENT", type="number", placeholder=" "),
                dbc.Label("Effective balance increment (ETH)")], className="input-label-float")]),
            ], justify="start"
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="PROPOSER_REWARD_QUOTIENT", type="number", placeholder=" "),
                dbc.Label("Proposer reward quotient")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="WHISTLEBLOWER_REWARD_QUOTIENT", type="number", placeholder=" "),
                dbc.Label("Whistleblower reward quotient")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="MIN_SLASHING_PENALTY_QUOTIENT", type="number", placeholder=" "),
                dbc.Label("Min slashing penalty quotient")], className="input-label-float")]),

                dbc.Col([
                dbc.Button("Use default values",
                            id="button-eth2-specs-default",
                            className="button")])
            ], justify="start"
        )],id="collapse-eth2")
    ]   
)