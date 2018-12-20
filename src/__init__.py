import os
import requests
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
@app.route("/<string:stock_name>") # TODO: need to change route name
def chart(stock_name):
    data = get_data(stock_name)
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    seqs = np.arange(df.shape[0])
    import pdb; pdb.set_trace()
    df['seqs'] = pd.Series(seqs)
    df['changePercent'] = df['changePercent'].apply(lambda x: str(x)+'%')
    df['mid'] = df.apply(lambda x: (x['open'] + x['close'])/2, axis = 1)
    df['height'] = df.apply(
        lambda x: x['close'] - x['open'] if x['close'] != x['open'] else 0.01,
        axis = 1)
    inc = df.close > df.open
    dec = df.close < df.open
    w = .3
    sourceInc = bk.ColumnDataSource(df.loc[inc])
    sourceDec = bk.ColumnDataSource(df.loc[dec])

    hover = HoverTool(
        tooltips=[
        ('Date', '@date'),
        ('Low', '@low'),
        ('High', '@high'),
        ('Open', '@open'),
        ('Close', '@close'),
        ('Percent', '@changePercent'),
        ])
    TOOLS = []
    # TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(), ZoomOutTool(), ResetTool()]
    p = figure(plot_width = 1000, plot_height = 800, title = stock_name, tools=TOOLS, toolbar_location = 'above')
    p.xaxis.major_label_orientation = np.pi/4

    # set gird line width
    p.grid.grid_line_alpha = w
    p.segment(df.seqs[inc],df.high[inc], df.seqs[inc], df.low[inc], color = 'green')
    p.segment(df.seqs[dec],df.high[dec], df.seqs[dec], df.low[dec], color = 'red')
    p.rect(x='seqs', y='mid', width=w, height='height', fill_color='red', line_color='red', source=sourceDec)
    p.rect(x='seqs', y='mid', width=w, height='height', fill_color='green', line_color='green', source=sourceInc)

    descriptor = Label(x=70, y=70, text=f"5-year stock chart of {stock_name}")
    p.add_layout(descriptor)
    script, div = components(p)
    return render_template("chart.html", stock_name=stock_name,
                            the_div=div, the_script=script)

def get_data(stock_name):
    """
    """
    API_URL = 'https://api.iextrading.com/1.0'
    res = requests.get(f'{API_URL}/stock/{stock_name}/chart/5y')
    data =res.json()
    return data


