import os
import requests
import json
import numpy as np
from math import pi
import pandas as pd
import bokeh.plotting as bk
from bokeh.embed import components
from bokeh.transform import transform
from flask import Flask, render_template
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file #, show
from bokeh.models import Label, HoverTool, BoxZoomTool, PanTool, ZoomInTool, ZoomOutTool, ResetTool
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter

# get root of the project. The benefit is path is not hard coded and shall be adaptable.
basedir = os.path.abspath(os.path.dirname(__file__))

# create app
app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    instance_relative_config=True, # allows config to be in the flask app
)

app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# mont config from source directory
from . import routes, auth, forms, models, exceptions

# 12/19/18 new
