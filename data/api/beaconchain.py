import requests
import diskcache

from model.types import Gwei


cache = diskcache.Cache('.beaconchain_api.cache')

@cache.memoize(expire=(6 * 60 * 60))  # cached for 6 hours
def get_epoch_data(epoch="latest"):
    return requests.get(f"https://beaconcha.in/api/v1/epoch/{epoch}", headers={"accept":"application/json"}).json()["data"]

def get_total_validator_balance() -> Gwei:
    return int(get_epoch_data()["totalvalidatorbalance"])

def get_validators_count() -> int:
    return int(get_epoch_data()["validatorscount"])
