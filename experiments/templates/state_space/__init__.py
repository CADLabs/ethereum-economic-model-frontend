from model.types import Stage
import model.constants as constants
import model.simulation_configuration as simulation_configuration
from model.stochastic_processes import create_stochastic_process_realizations
from model.types import Stage
from experiments.base import experiment


DELTA_TIME = constants.epochs_per_day  # epochs per timestep
SIMULATION_TIME_MONTHS = 12 * 5  # number of months
TIMESTEPS = constants.epochs_per_month * SIMULATION_TIME_MONTHS // DELTA_TIME

# Generate stochastic process realizations
stochastic_process_realizations = create_stochastic_process_realizations(TIMESTEPS, DELTA_TIME)
eth_price_samples = stochastic_process_realizations['eth_price_samples']

parameter_overrides = {
    "stage": [Stage.ALL],
    "eth_price_process": [lambda run, timestep: eth_price_samples[run - 1][timestep]],
}

experiment.simulations[0].timesteps = TIMESTEPS
# Override base experiment System Parameters
experiment.simulations[0].model.params.update(parameter_overrides)
