# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash, html, dcc
import pandas as pd

import subprocess

DOWNLOAD_INC_FILE_PATH = 'incubation_chamber.csv'
SAVE_FILE_PATH = 'ass.csv'

app = Dash(__name__)

colors = {
    'background': '#282828',
    'text': '#ebdbb2'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(
    style={
        'backgroundColor': colors['background']
    },
    children=[
        html.H1(children='Hello Dash',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }),

        html.Div(children='''
            Dash: A web application framework for your data.
        ''',
                 style={
                     'textAlign': 'center',
                     'color': colors['text']
                 }),

        dcc.Graph(
            id='humidity-graph',
            style={'width': '170vh', 'height': '90vh'}
        ),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        )
    ])


@app.callback(
    Output('humidity-graph', 'figure'),
    Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    subprocess.call(["./download.sh", DOWNLOAD_INC_FILE_PATH, SAVE_FILE_PATH],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    df = pd.read_csv(SAVE_FILE_PATH)
    # fig.update_traces(overwrite=True)
    fig = make_subplots(rows=2, cols=2)
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['hum']),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['rand']),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['hum']),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['rand']),
        row=2, col=2
    )

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
