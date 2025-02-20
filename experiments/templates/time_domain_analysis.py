import copy

import ethereum_economic_model.model.constants as constants
from ethereum_economic_model.model.stochastic_processes import create_stochastic_process_realizations
from ethereum_economic_model.model.types import Stage
from ethereum_economic_model.experiments.default_experiment import experiment


# Make a copy of the default experiment to avoid mutation
experiment = copy.deepcopy(experiment)

DELTA_TIME = constants.epochs_per_day  # epochs per timestep
SIMULATION_TIME_MONTHS = 12 * 5  # number of months
TIMESTEPS = constants.epochs_per_month * SIMULATION_TIME_MONTHS // DELTA_TIME

# Generate stochastic process realizations
eth_price_samples = create_stochastic_process_realizations("eth_price_samples", timesteps=TIMESTEPS, dt=DELTA_TIME)

parameter_overrides = {
    "stage": [Stage.ALL],
    "eth_price_process": [lambda run, timestep: eth_price_samples[run - 1][timestep]],
}

experiment.simulations[0].timesteps = TIMESTEPS
# Override default experiment System Parameters
experiment.simulations[0].model.params.update(parameter_overrides)
