import dash
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import get_risk
import yfinance as yf
import get_prices
import dash_table


#import get_returns

app = Dash(__name__)

#list_symbols = ['WEGE3.SA', 'TASA4.SA', 'PRIO3.SA']
#prices = pd.DataFrame()
#prices = yf.download(list_symbols, start='2000-01-01')['Adj Close'].fillna(0).reset_index()
tickers_list = list(set(get_prices.get_tickers()))

#returns,b = get_returns.log_return(prices)

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

    html.Div(id='selected_tickers', className='table'),    
    ],

    #html.Div(children=[
    #    html.Br(),
    #    html.Label('Prices table'),
    #    table(prices)])],

    #html.Div(id = "teste",
    #children=[
    #    html.Br(),
    #    html.Label('Returns table'),
    #    table(returns)])],

    style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(
    Output('selected_tickers', 'children'),
    Input('tickers_dropdown', 'value'),
    prevent_initial_call=True
)
def get_some_prices(selected_tickers):
    prices = yf.download(selected_tickers, start = '2015-01-01')['Adj Close'].fillna(0).reset_index()
    col = [{'name': i, 'id': i} for i in prices.columns]
    table = dash_table.DataTable(
            id='table',
            columns = col,
            page_size= 6,
            style_cell={'width': '45'},
            data = prices.to_dict('records')
    )
    return table

dash_table.DataTable()

'''
    df_chart = df.groupby('Name').sum()
    return [
        dt.DataTable(
            rows=df_chart.to_dict('rows'),
            columns=df_chart.columns,
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=list(df_chart.index),  # all rows selected by default
            id='3'
        )
'''
if __name__ == '__main__':
    app.run_server(debug=True)