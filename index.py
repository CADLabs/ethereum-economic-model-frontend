from app import app

from layout.eth2_specs.eth2_specs_callbacks import toggle_collapse_eth2
from layout.validator_specs.validator_specs_callbacks import (toggle_collapse_validator,
                                                              load_validator_specs_defaults,
                                                              calc_total_validator_distribution)
from layout.output_graphs.output_graphs_callbacks import run_simulation


if __name__ == "__main__":
    app.run_server(debug=True)
