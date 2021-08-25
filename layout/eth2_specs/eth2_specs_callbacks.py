from dash.dependencies import Input, Output, State

from app import app
from model.system_parameters import parameters

@app.callback(
    Output("collapse-eth2", "is_open"),
    [Input("collapse-button-eth2", "n_clicks")],
    [State("collapse-eth2", "is_open")],
)
def toggle_collapse_eth2(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("BASE_REWARD_FACTOR", "value"),
    Output("MAX_EFFECTIVE_BALANCE", "value"),
    Output("EFFECTIVE_BALANCE_INCREMENT", "value"),
    Output("PROPOSER_REWARD_QUOTIENT", "value"),
    Output("WHISTLEBLOWER_REWARD_QUOTIENT", "value"),
    Output("MIN_SLASHING_PENALTY_QUOTIENT", "value"),
    [Input("button-eth2-specs-default", "n_clicks")]
)
def load_eth2_specs_defaults(n_clicks):
    base_reward_factor = parameters['BASE_REWARD_FACTOR'][0]
    max_effective_balance = parameters['MAX_EFFECTIVE_BALANCE'][0]/1e9
    effective_balance_increment = parameters['EFFECTIVE_BALANCE_INCREMENT'][0]/1e9
    proposer_reward_quotient = parameters['PROPOSER_REWARD_QUOTIENT'][0]
    whistleblower_reward_quotient = parameters['WHISTLEBLOWER_REWARD_QUOTIENT'][0]
    min_slashing_penalty_quotient = parameters['MIN_SLASHING_PENALTY_QUOTIENT'][0]

    return (base_reward_factor, 
            max_effective_balance, effective_balance_increment, proposer_reward_quotient,
            whistleblower_reward_quotient, min_slashing_penalty_quotient)