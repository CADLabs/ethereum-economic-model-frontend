# Dash dependencies
import dash
import dash_bootstrap_components as dbc

import flask

# Plotly custom theme
import plotly.io as pio
from assets import plotly_theme
pio.templates.default = "cadlabs_frontend"

# Import layout components
from layout.layout import layout


server = flask.Flask(__name__) # define flask app.server



app = dash.Dash(__name__,
                server=server,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.LUX])
    
app.title = "Eth2 Calculator"
app.layout = layout
