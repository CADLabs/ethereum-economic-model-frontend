import argparse

from app import app
from utils.auth import load_basic_auth


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', default=False, action='store_true')
    args = parser.parse_args()

    if not args.dev:
        load_basic_auth(app)

    app.run_server(debug=False)
