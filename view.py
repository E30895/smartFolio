from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


'''
Esse módulo fornece recursos de visualização: gráficos, layout[...]
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

def plot_efficient_frontier(wallets: dict, best_return_vol: tuple) -> go.Figure:
    fig = make_subplots(shared_yaxes=True, shared_xaxes=True)
    fig.add_scatter(x=wallets['vol'], y=wallets['returns'], name='Carteiras')
    fig.add_scatter(x=[best_return_vol[1]], y=[best_return_vol[0]], name='Carteira Ótima', marker_size = 10)
    fig.update_traces(mode='markers', hovertemplate='Retorno: %{y}'+ '<br>Risco: %{x}')
    fig.update_layout(title='Fronteira Eficiente', xaxis_title='Risco', yaxis_title='Retorno')

    return fig

def layout_creator(tickers, intervals):
    return html.Div([

    html.Div([
        html.H1('smartFolio'),
        html.Img(src='/assets/stocks.png')
    ], className='banner'),

    html.Div(children=[
        html.Br(),
        html.Label('Selecione os tickers (mínimo 2)'),
        dcc.Dropdown(tickers,
                     multi=True, 
                     id='tickers_dropdown'
                     )
                     ], style={'padding': 10, 'flex': 1, 'textAlign':'center'}),
    
    html.Div(children=[
        
        html.Br(),

        html.Label('Insira a data inicial'),
        dcc.Input(id='start_date', type='text', placeholder="Formato: YYYY-MM-DD"),
        
        html.Label('Insira a data final (Opcional)'), 
        dcc.Input(id='end_date', type='text', placeholder="Formato: YYYY-MM-DD"),

        html.Br(),
        
        html.Label('Selecione o intervalo'),
        dcc.Dropdown(intervals, id='intervals_dropdown'),

        html.Button('Enviar', id='submit_button'),
    
    ], style={'padding': 10, 'flex': 1, 'textAlign':'center'}),

    html.Div(id='selected_tickers', className='table'),    
    
    dcc.Graph(id='returns_fig'),
    
    html.Div([
        html.H4('Tabela de Pesos dos Ativos')
    ]),

    html.Div(id='weights_table', className='table'),

    dcc.Graph(id='efficient_frontier')
    ],

    style={'display': 'flex', 'flex-direction': 'column'})
