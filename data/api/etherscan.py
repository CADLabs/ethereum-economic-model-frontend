import requests
import diskcache
import os
from dotenv import load_dotenv

from model.types import Wei

load_dotenv()
cache = diskcache.Cache('.etherscan_api.cache')

@cache.memoize(expire=(6 * 60 * 60))  # cached for 6 hours
def get_eth_supply() -> Wei:
    return int(requests.get("https://api.etherscan.io/api?module=stats&action=ethsupply", headers={"accept": "application/json", "apikey":os.environ.get('ETHERSCANAPIKEY')}).json()["result"])
