from dash.dependencies import Input, Output, State

from model.system_parameters import parameters

from app import app



@app.callback(
    Output("collapse-validator", "is_open"),
    [Input("collapse-button-validator", "n_clicks")],
    [State("collapse-validator", "is_open")],
)
def toggle_collapse_validator(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("validator_internet_uptime", "value"),
    Output("diy_hardware_distribution", "value"),
    Output("diy_cloud_distribution", "value"),
    Output("pool_staas_distribution", "value"),
    Output("pool_hardware_distribution", "value"),
    Output("pool_cloud_distribution", "value"),
    Output("staas_full_distribution", "value"),
    Output("staas_self_custodied_distribution", "value"),
    Output("diy_hardware_cost", "value"),
    Output("diy_cloud_cost", "value"),
    Output("pool_staas_cost", "value"),
    Output("pool_hardware_cost", "value"),
    Output("pool_cloud_cost", "value"),
    Output("staas_full_cost", "value"),
    Output("staas_self_custodied_cost", "value"),
    Output("validator_distribution_weighted_avg_cost", "value"),
    [Input("button-validator-specs-default", "n_clicks")]
)
def load_validator_specs_defaults(n_clicks):
    validator_internet_uptime = 100 * parameters['validator_uptime_process'][0](0,0)
    diy_hardware_distribution = 100 * parameters['validator_percentage_distribution'][0][0]
    diy_cloud_distribution = 100 * parameters['validator_percentage_distribution'][0][1]
    pool_staas_distribution = 100 * parameters['validator_percentage_distribution'][0][2]
    pool_hardware_distribution = 100 * parameters['validator_percentage_distribution'][0][3]
    pool_cloud_distribution = 100 * parameters['validator_percentage_distribution'][0][4]
    staas_full_distribution = 100 * parameters['validator_percentage_distribution'][0][5]
    staas_self_custodied_distribution = 100 * parameters['validator_percentage_distribution'][0][6]

    diy_hardware_cost = parameters['validator_hardware_costs_per_epoch'][0][0]
    diy_cloud_cost = parameters['validator_cloud_costs_per_epoch'][0][1]
    pool_staas_cost = parameters['validator_third_party_costs_per_epoch'][0][2]
    pool_hardware_cost = parameters['validator_hardware_costs_per_epoch'][0][3]
    pool_cloud_cost = parameters['validator_cloud_costs_per_epoch'][0][4]
    staas_full_cost = parameters['validator_third_party_costs_per_epoch'][0][5]
    staas_self_custodied_cost = parameters['validator_third_party_costs_per_epoch'][0][6]
    validator_distribution_weighted_avg_cost = sum([diy_hardware_distribution * diy_hardware_cost,
                                                    diy_cloud_distribution * diy_cloud_cost, 
                                                    pool_staas_distribution * pool_staas_cost,
                                                    pool_hardware_distribution * pool_hardware_cost,
                                                    pool_cloud_distribution * pool_cloud_cost,
                                                    staas_full_distribution * staas_full_cost,
                                                    staas_self_custodied_distribution * staas_self_custodied_cost
                                                    ])/100

    return (validator_internet_uptime, 
            diy_hardware_distribution,
            diy_cloud_distribution, pool_staas_distribution,
            pool_hardware_distribution, pool_cloud_distribution,
            staas_full_distribution, staas_self_custodied_distribution,
            diy_hardware_cost, diy_cloud_cost,
            pool_staas_cost, pool_hardware_cost, pool_cloud_cost,
            staas_full_cost, staas_self_custodied_cost,
            validator_distribution_weighted_avg_cost)


@app.callback(
    Output("validator_total_distribution", "value"),
    [Input("diy_hardware_distribution", "value"),
    Input("diy_cloud_distribution", "value"),
    Input("pool_staas_distribution", "value"),
    Input("pool_hardware_distribution", "value"),
    Input("pool_cloud_distribution", "value"),
    Input("staas_full_distribution", "value"),
    Input("staas_self_custodied_distribution", "value")]
)
def calc_total_validator_distribution(diy_hardware_distribution,
                                      diy_cloud_distribution,
                                      pool_staas_distribution,
                                      pool_hardware_distribution,
                                      pool_cloud_distribution,
                                      staas_full_distribution,
                                      staas_self_custodied_distribution):

    validator_distribution = [diy_hardware_distribution,
                                        diy_cloud_distribution, 
                                        pool_staas_distribution,
                                        pool_hardware_distribution,
                                        pool_cloud_distribution,
                                        staas_full_distribution,
                                        staas_self_custodied_distribution]
 
    non_empty_validators = list(filter(None, validator_distribution))
    validator_total_distribution = sum(non_empty_validators)

    return validator_total_distribution