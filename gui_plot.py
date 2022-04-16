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
        html.H1(children='Shroomery',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'backgroundColor': colors['background']
                }),

        html.Div(children='''
            ShroomRoom
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
            interval=1*1500,  # in milliseconds
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
    # fig = make_subplots(rows=4, cols=2)
    fig = make_subplots(rows=2, cols=2)
    fig.add_trace(
        go.Scatter(name="CO2",
                   x=df['time'],
                   y=df['co2'],
                   line=go.Line(color='#8ec07c',
                                width=6),
                   ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(name="Humidity",
                   x=df['time'],
                   y=df['humidity'],
                   line=go.Line(color='#b16286',
                                width=6)),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(name="Temperature",
                   x=df['time'],
                   y=df['temperature'],
                   line=go.Line(color='#d79921',
                                width=6)),
        row=2, col=1
    )
    """
    fig.add_trace(
        go.Scatter(x=df['time'][:50],
                   y=df['time'][:50],
                   line=go.Line(color='#458588',
                                width=6)),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=df['time'][:50],
                   y=df['co2'][:50],
                   line=go.Line(color='#355629',
                                width=6),
                   ),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=df['time'][:50],
                   y=df['humidity'][:50],
                   line=go.Line(color='#67324a',
                                width=6)),
        row=3, col=2
    )
    fig.add_trace(
        go.Scatter(x=df['time'][:50],
                   y=df['temperature'][:50],
                   line=go.Line(color='#845f15',
                                width=6)),
        row=4, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['time'][:50],
                   y=df['time'][:50],
                   line=go.Line(color='#224244',
                                width=6)),
        row=4, col=2
    )
    """
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
    )
    fig.update_xaxes(showgrid=True,
                     gridwidth=1,
                     gridcolor='#928374',
                     # tickvals=range(50, step=10),
                     showticklabels=False)
    fig.update_yaxes(showgrid=True,
                     gridwidth=1,
                     gridcolor='#928374')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
