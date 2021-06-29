import dash_html_components as html
import dash_bootstrap_components as dbc
from layout.eth2_specs.eth2_specs import eth2_specs
from layout.exogenous_processes.exogenous_processes import exogenous_processes
from layout.output_graphs.output_graphs import output_graphs
from layout.validator_specs.validator_specs import validator_uptime, validator_percentage_distribution

card_graph = dbc.Card(
    dbc.FormGroup(
        [
        exogenous_processes,
        eth2_specs,
        dbc.Collapse([
        html.Hr(),
        validator_uptime,
        html.Hr(),
        validator_percentage_distribution], id="collapse-validator"),
        html.Hr(),
        output_graphs
        ]
), body=True, color="#272838")

layout = html.Div([
    dbc.Row([dbc.Col(html.H1("Eth2 Staking Calculator", style={"color": "white"}), width=10)], justify="around"),
    dbc.Row([dbc.Col(card_graph, width=10)], justify="around"),
],
   className="outer-background"
)