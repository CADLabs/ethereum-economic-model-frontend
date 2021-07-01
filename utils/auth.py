import os
from dotenv import load_dotenv
import dash_auth



load_dotenv()
def load_basic_auth(app):
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    VALID_USERNAME_PASSWORD_PAIRS = {
        USERNAME: PASSWORD
    }

    auth = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS
    )
