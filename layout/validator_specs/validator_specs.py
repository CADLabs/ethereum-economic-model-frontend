import dash_html_components as html
import dash_bootstrap_components as dbc

validator_uptime = html.Div(
    [
        html.H3('Validator Parameters', style={"color": "white"}),
        html.Hr(className="under-title"),
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                dbc.Input(id="validator_internet_uptime", type="number", placeholder=" "),
                dbc.Label("Validator internet uptime (%)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="validator_power_uptime", type="number", placeholder=" "),
                dbc.Label("Validator power uptime (%)")], className="input-label-float")]),

                dbc.Col([
                html.Div([
                dbc.Input(id="validator_technical_uptime", type="number", placeholder=" "),
                dbc.Label("Validator technical uptime (%)")], className="input-label-float")]),

                dbc.Col([
                dbc.Button("Use default values",
                            id="button-validator-specs-default",
                            className="button")])
            ], justify="start"
        ),
    ]
)

validator_percentage_distribution = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                dbc.Card([    
                html.H4('Validators distribution', style={"color": "white"}), 
                dbc.Row([
                    html.Div([
                    dbc.Input(id="diy_hardware_distribution", type="number", placeholder=" "),
                    dbc.Label("DIY hardware (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="diy_cloud_distribution", type="number", placeholder=" "),
                    dbc.Label("DIY cloud (%)")], className="input-label-float", style={"width":"200px"})
                ], justify="around"),
                dbc.Row([
                    html.Div([
                    dbc.Input(id="pool_staas_distribution", type="number", placeholder=" "),
                    dbc.Label("Pool StaaS (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="pool_hardware_distribution", type="number", placeholder=" "),
                    dbc.Label("Pool hardware (%)")], className="input-label-float", style={"width":"200px"})
                ], justify="around"),
                dbc.Row([
                    html.Div([
                    dbc.Input(id="pool_cloud_distribution", type="number", placeholder=" "),
                    dbc.Label("Pool cloud (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="staas_full_distribution", type="number", placeholder=" "),
                    dbc.Label("StaaS full (%)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                dbc.Row([
                    html.Div([
                    dbc.Input(id="staas_self_custodied_distribution", type="number", placeholder=" "),
                    dbc.Label("StaaS self custodied (%)")], className="input-label-float", style={"width":"200px"}),
                    html.Div([
                    dbc.Input(id="validator_total_distribution", type="number", placeholder=" "),
                    dbc.Label("Total(%)")], className="input-label-float", style={"width":"200px"})
                ], justify="around"),
                ], className="validator-card")]),

                dbc.Col([
                    dbc.Card([    
                    html.H4('Validation cost', style={"color": "white"}), 
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="diy_hardware_cost", type="number", placeholder=" "),
                        dbc.Label("DIY hardware ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="diy_cloud_cost", type="number", placeholder=" "),
                        dbc.Label("DIY cloud ($)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="pool_staas_cost", type="number", placeholder=" "),
                        dbc.Label("Pool StaaS ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="pool_hardware_cost", type="number", placeholder=" "),
                        dbc.Label("Pool hardware ($)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="pool_cloud_cost", type="number", placeholder=" "),
                        dbc.Label("Pool cloud ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="staas_full_cost", type="number", placeholder=" "),
                        dbc.Label("StaaS full ($)")], className="input-label-float", style={"width":"200px"})
                        ], justify="around"),
                    dbc.Row([
                        html.Div([
                        dbc.Input(id="staas_self_custodied_cost", type="number", placeholder=" "),
                        dbc.Label("StaaS self custodied ($)")], className="input-label-float", style={"width":"200px"}),
                        html.Div([
                        dbc.Input(id="validator_distribution_weighted_avg_cost", type="number", placeholder=" "),
                        dbc.Label("Weighted average cost ($)")], className="input-label-float", style={"width":"200px"})
                    ], justify="around"),
                    ], className="validator-card")]),
            ]
        )
    ]
)