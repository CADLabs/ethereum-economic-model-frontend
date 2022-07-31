# CADLabs Ethereum Validator Economics Model Dashboard

## Table of Contents
* [Directory Structure](#directory-structure)
* [Development](#development)
* [Deployment](#deployment)

---

## Directory Structure
* [assets/](assets/): CSS styles and assets
* [data/](data/): preloaded datasets used by the dashboard
* [experiments/](experiments/): experiment workflow configuration and execution
* [model/](model/): model structure, parts, and configuration

## Development
### Requirements

* Python versions: tested with 3.7, 3.8, 3.9
* Python dependencies: tested against versions in `requirements.txt`

### Setup

To setup a Python 3 development environment:
```bash
# Create a virtual environment using Python 3 venv module
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Install Python 3 dependencies inside virtual environment
pip install -r requirements.txt
```

### Local Execution

To execute the dashboard locally:
```bash
python index.py
```
To execute the dashboard in the development version (without authentication):
```bash
python index.py --dev
```

After executing the command, the dash app will run locally. The default dash port is http://127.0.0.1:8050/.

## Deployment

The current version of the dashboard is deployed at https://eth2-calculator.herokuapp.com/.
