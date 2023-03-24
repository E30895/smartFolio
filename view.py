from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import plotly.express as px
import pandas as pd
import numpy as np


'''
Esse módulo fornece recursos de visualização: gráficos, laytout[...]
'''

def fig_line(data, selected_tickers):
    fig = px.line(data, x = "Date", y = selected_tickers)
    return fig

def table(dataframe: pd.DataFrame, max_rows=10):
    col = [{'name': i, 'id': i} for i in dataframe.columns]
    table = dash_table.DataTable(
            id='table',
            columns = col,
            page_size = 6,
            style_cell={'width': '45'},
            data = dataframe.to_dict('records')
            )
    return table

def layout_creator(tickers, intervals):
    return html.Div([

    html.Div([
        html.H1('smartFolio'),
        html.Img(src='/assets/stocks.png')
    ], className='banner'),

    html.Div(children=[
        html.Br(),
        html.Label('Select multiple tickers'),
        dcc.Dropdown(tickers,
                     multi=True, 
                     id='tickers_dropdown'
                     )
                     ], style={'padding': 10, 'flex': 1, 'textAlign':'center'}),
    
    html.Div(children=[
        
        html.Br(),

        html.Label('Select start date'),
        dcc.Input(id='start_date', type='text', placeholder="YYYY-MM-DD format"),
        
        html.Label('Select end date (Optional)'), 
        dcc.Input(id='end_date', type='text', placeholder="YYYY-MM-DD format"),

        html.Br(),
        
        html.Label('Select interval'),
        dcc.Dropdown(intervals, id='intervals_dropdown'),

        html.Button('Submit', id='submit_button'),
    
    ], style={'padding': 10, 'flex': 1, 'textAlign':'center'}),

    html.Div(id='selected_tickers', className='table'),    
    dcc.Graph(id='grafico')
    ],

    style={'display': 'flex', 'flex-direction': 'column'})
