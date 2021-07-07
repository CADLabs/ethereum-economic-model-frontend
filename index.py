import argparse

from app import app, server
from utils.auth import load_basic_auth
from layout.eth2_specs.eth2_specs_callbacks import toggle_collapse_eth2
from layout.validator_specs.validator_specs_callbacks import (toggle_collapse_validator,
                                                              load_validator_specs_defaults,
                                                              calc_total_validator_distribution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', default=False, action='store_true')
    args = parser.parse_args()

    if not args.dev:
        load_basic_auth(app)

    app.run_server(debug=False)
