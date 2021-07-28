import sys
import copy
import logging
import numpy as np
import pandas as pd
from datetime import datetime
import itertools
import json

#import setup

# Append the root directory to Python path,
sys.path.append("../..")
sys.path.append("../../..")

from experiments.run import run
from model.types import Stage

from data.historical_values import df_ether_supply

logger = logging.getLogger()

# Import experiment templates
import experiments.templates.json_generator_setup as json_generator_setup

# Fetch the time-domain analysis experiment
experiment = json_generator_setup.experiment
# Create a copy of the experiment simulation
simulation = copy.deepcopy(experiment.simulations[0])

# Define parameter_object class
class parameter_object:
    def __init__(self, parameter_definition):
        self.parameter = parameter_definition['parameter']
        self.label = parameter_definition['label']
        self.points = parameter_definition['points']
        self.init_index = parameter_definition['init_index']
        self.function = parameter_definition['function']
        self.process_expand()

    def process_expand(self):
        self.processes = [self.function(x) for x in self.points]

    def process_generator_constant_value(x):
        return lambda _run, _timestep: x

    def process_time(x):
        return datetime.strptime(x, "%Y-%m-%d")
    
    def info(self):
        return {
            'label': self.label,
            'parameter': self.parameter,
            'points': self.points
        }


# Define processes
date_pos_points = parameter_object({
    'parameter': 'date_pos',
    'label': 'Proof of Stake Initialization Date',
    'points': ["2021-12-1", "2022-3-1", "2022-6-1", "2022-9-1", "2022-12-1", "2023-3-1", "2023-6-1"],
    'init_index': 2,
    'function': parameter_object.process_time
})


eip1559_basefee_process_points = parameter_object({
    'parameter': 'eip1559_basefee_process',
    'label': 'EIP-1559 Base Fee',
    'points': np.arange(0, 110, 10).tolist(),
    'init_index': 2,
    'function': parameter_object.process_generator_constant_value
})

validator_process_points = parameter_object({
    'parameter': 'validator_process',
    'label': 'Validator Adoption Rate',
    'points': np.arange(0, 8, 0.5).tolist(),
    'init_index': [1],
    'function': parameter_object.process_generator_constant_value
})

# Collect processes for simulation
parameter_sweep_list = [
    date_pos_points,
    eip1559_basefee_process_points,
    validator_process_points
]


# Define important dates
historical_dates = {
    "Frontier" : "2015-7-30",
    "Frontier thawing" : "2015-9-7",
    "Homestead" : "2016-3-14",
    "Byzantium" : "2017-10-16",
    "Constantinople" : "2019-2-28",
    "Istanbul" : "2019-12-8",
    "Muir Glacier" : "2020-1-2",
    "Beacon Chain Genesis" : "2020-12-01",
    "EIP1559" : "2021-07-14"
}


# Define custom cartesian product generator to handle meta data
def generate_cartesian_product_parameter_sweep_from_parameter_object(object_list):
    points_list = []
    for object_id,process_object in enumerate(object_list):
        sub_points_list = []
        for point_id,point in enumerate(process_object.points):
            sub_points_list.append((object_id, point_id))
        points_list.append(sub_points_list)


    cartesian_product = list(itertools.product(*points_list))
    params = {parameter_object.parameter: [object_list[x[i][0]].processes[x[i][1]] for x in cartesian_product] for i, parameter_object in enumerate(object_list)}
    lookup = [[x[i][1] for x in cartesian_product] for i, parameter_object in enumerate(object_list)]

    return params, lookup

# Generate cartesion product to create all permuations of inputs
simulation_list, lookup = generate_cartesian_product_parameter_sweep_from_parameter_object(parameter_sweep_list)

# Update simulation to include newly generated simulations
simulation.model.params.update(simulation_list)

# Run simulations
df, _exceptions = run(simulation)

# Pre-process historic eth supply data, aggregating to weekly data
def grab_last_sample(data):
    return data[-1]

df_ether_supply = df_ether_supply.drop('timestamp', axis=1)
df_ether_supply = df_ether_supply.resample('W', origin='epoch').apply(grab_last_sample)
df_ether_supply.reset_index(inplace=True)

# Convert timestamp to string
df_ether_supply.timestamp = df_ether_supply.timestamp.dt.strftime('%Y-%m-%d')
# Convert eth supply to integer
df_ether_supply.eth_supply = df_ether_supply.eth_supply.astype(int)

# Convert simulated data timestamp to string
df.timestamp = df.timestamp.dt.strftime('%Y-%m-%d')
# Convert eth supply to integers
df.eth_supply = df.eth_supply.astype(int)


# Generate dictionary from historic and simulated data

results_dict = {}
param_dict = {}
for id,param in enumerate(parameter_sweep_list):
    param_dict[id] = param.info()


info_dict={}
info_dict['parameters'] = param_dict

aux_dict = {}
aux_dict['historical_dates'] = historical_dates

info_dict['aux'] = aux_dict

results_dict['info'] = info_dict

history_dict={}
history_dict['timestamp'] = df_ether_supply.timestamp.unique().tolist()
history_dict['supply_inflation_pct'] = df_ether_supply.supply_inflation_pct.values.tolist()
history_dict['eth_supply'] = df_ether_supply.eth_supply.values.tolist()


data_dict={}

sim_dict={}
sim_dict['timestamp'] = df.timestamp.unique().tolist()

for subset in df.subset.unique():
    subset_key_info = []
    delimiter = ":"
    for param_id in range(len(parameter_sweep_list)):
        subset_key_info.append(str(parameter_sweep_list[param_id].points[lookup[param_id][subset]]))
    df_subset = df.query(f"subset=={subset}")
    sim_dict[delimiter.join(subset_key_info)] = {
        'supply_inflation_pct' :df_subset.supply_inflation_pct.values.tolist(),
        'eth_supply': df_subset.eth_supply.values.tolist()
    }
    
data_dict['simulations'] = sim_dict
data_dict['historical'] = history_dict
results_dict['data'] = data_dict


# Write dictionary as json file
with open("supply.json", "w") as outfile: 
    json.dump(results_dict, outfile, indent=4)

print("supply.json generated")
