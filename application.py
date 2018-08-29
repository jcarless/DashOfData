import dash
from flask import render_template
from flask import request
from flask import Flask, url_for
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from datetime import datetime
import base64

# application = server = Flask("myserver")
# app = dash.Dash(server=server)

app = dash.Dash(__name__)
application = app.server

IMAGE_FOLDER = os.path.join('static', 'ComingSoon')

image_filename = './static/ComingSoon/ComingSoon.png'

app.layout = html.Div([
    html.Img(src=image_filename, width='100%')
])

if __name__ == '__main__':
    app.run_server(debug=True)
