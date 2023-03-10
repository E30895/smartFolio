import dash
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np
import get_risk
import yfinance as yf
import get_prices
#import get_returns

app = Dash(__name__)

list_symbols = ['WEGE3.SA', 'TASA4.SA', 'PRIO3.SA']
prices = pd.DataFrame()
prices = yf.download(list_symbols, start='2000-01-01')['Adj Close'].fillna(0).reset_index()
tickers_list = get_prices.get_tickers()

#returns,b = get_returns.log_return(prices)

def table(prices: pd.DataFrame, max_rows=10):
   #data.sort_values(by=date, ascending= False)
   return html.Table([
        
        #CABEÇALHOS
        html.Thead(
            html.Tr([html.Th(col) for col in prices.columns])
        ),
        
        #CORPO
        html.Tbody([
            html.Tr([
                html.Td(prices.iloc[i][col]) for col in prices.columns
            ]) for i in range(min(len(prices), max_rows))
        ])
    ])

###### LAOUT ############

app.layout = html.Div([

    html.Div([
        html.H1('smartFolio'),
        html.Img(src='/assets/stocks.png')
    ], className='banner'),

    html.Div(children=[
        html.Br(),
        html.Label('Select your ticker'),
        dcc.Dropdown(tickers_list, #PASSA UMA LISTA DE TICKERS
                     multi=True, 
                     id='tickers_dropdown'
                     )], 
                     style={'padding': 10, 'flex': 1, 'textAlign':'center'}),
                     

    html.Div(children=[
        html.Br(),
        html.Label('Prices table'),
        table(prices)])],

    #html.Div(id = "teste",
    #children=[
    #    html.Br(),
    #    html.Label('Returns table'),
    #    table(returns)])],

       style={'display': 'flex', 'flex-direction': 'column'})


if __name__ == '__main__':
    app.run_server(debug=True)