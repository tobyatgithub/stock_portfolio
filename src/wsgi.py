from . import app
import os
import requests
from json import JSONDecodeError
import numpy as np
from math import pi
import pandas as pd
import bokeh.plotting as bk
from bokeh.embed import components
from bokeh.transform import transform
from flask import Flask, render_template, abort
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file #, show
from bokeh.models import Label, HoverTool, BoxZoomTool, PanTool, ZoomInTool, ZoomOutTool, ResetTool
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter

@app.route("/charts/<" + stock_name + "/>", methods = ['GET']) # TODO: need to change route name
def generate_stock_graph_page(stock_name=None):
    pass
#     candle_script, candle_div, stock_name = make_candle_chart(stock_name)
#     circle_script, circle_div, stock_name = make_weight_graph(stock_name)
#     page_url = f'/charts/{ stock_name }.html'
#     return render_template(
#         page_url,
#         form=form,
#         symbol=form_context['symbol'],
#         company_data=session['context'],
#         stock_name = stock_name,
#         candle_div = candle_script,
#         candle_script = candle_div,
#         circle_div = circle_div,
#         circle_script = circle_script,
#     )

def make_candle_chart(stock_name=None):
    """
    """

    try:
        API_URL = 'https://api.iextrading.com/1.0'
        res = requests.get(f'{ API_URL }/stock/{ stock_name }/chart/5y')
        data = res.json()
    except JSONDecodeError:
        abort(404)
    df = pd.DataFrame(data)
    # df["date"] = pd.to_datetime(df["date"])
    # import pdb; pdb.set_trace()
    seqs = np.arange(df.shape[0])
    df['seqs'] = pd.Series(seqs)
    df['changePercent'] = df['changePercent'].apply(lambda x: str(x)+'%')
    df['mid'] = df.apply(lambda x: (x['open'] + x['close'])/2, axis = 1)
    df['height'] = df.apply(lambda x: x['close'] - x['open'] if x['close'] != x['open'] else 0.01, axis = 1)
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
        ], names = ["rect1","rect2"])

    TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(), ZoomOutTool(), ResetTool()]
    p = figure(plot_width = 1000, plot_height = 800, title = stock_name, tools=TOOLS, toolbar_location = 'above')
    p.xaxis.major_label_orientation = np.pi/4
    p.grid.grid_line_alpha = w
    # descriptor = Label(x=70, y=70, text=f"5-year stock chart of {stock_name}")
    # p.add_layout(descriptor)

    p.segment(df.seqs[inc],df.high[inc], df.seqs[inc], df.low[inc], color = 'green')
    p.segment(df.seqs[dec],df.high[dec], df.seqs[dec], df.low[dec], color = 'red')

    p.rect(x='seqs', y='mid', width=w, height='height', fill_color='red', line_color='red', source=sourceDec, name = "rect1")
    p.rect(x='seqs', y='mid', width=w, height='height', fill_color='green', line_color='green', source=sourceInc, name = "rect2")

    script, div = components(p)
    return script, div, stock_name
    # return render_template("chart.html", stock_name=stock_name, the_div=div, the_script=script)

def make_weight_graph(stock_name = None):
    """
    """
    try:
        API_URL = 'https://api.iextrading.com/1.0'
        res = requests.get(f'{ API_URL }/stock/{ stock_name }/chart/5y')
        data = res.json()
    except JSONDecodeError:
        abort(404)
    df = pd.DataFrame(data)
    # df['date'] = pd.to_datetime(df['date'])
    df['adjVolume'] = 6*df['volume']//df['volume'].mean()
    df = df[['date','vwap', 'volume','adjVolume']]
    seqs = np.arange(df.shape[0])
    df['seqs'] = pd.Series(seqs)

    source = ColumnDataSource(df)
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=df.adjVolume.min(), high=df.adjVolume.max())

    hover = HoverTool(
        tooltips=[
        ('Date', '@date'),
        ('Vwap', '@vwap'),
        ('Volume', '@volume'),
        ], names = ["circle"])

    TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(), ZoomOutTool(), ResetTool()]
    p = figure(plot_width=1000, plot_height=800, title= f'5 year weighted performace of {stock_name}',
            tools=TOOLS, toolbar_location = 'above')

    p.circle(x="seqs", y="vwap", source=source, size='adjVolume', fill_color=transform('adjVolume', mapper), name = "circle")
    color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                        ticker=BasicTicker(desired_num_ticks=len(colors)),
                        formatter=PrintfTickFormatter(format="%s%%"))
    p.add_layout(color_bar, 'right')

    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 1.0

    script, div = components(p)
    return script, div, stock_name



# here we handles the run part----let server run.
if __name__ =='__main__':
    app.run(debug=True)
