from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import get_risk
import yfinance as yf
import get_data
from datetime import datetime, date
#import get_returns

app = Dash(__name__)

tickers = get_data.get_tickers()
intervals = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']

###### LAYOUT ############

app.layout = html.Div([

    html.Div([
        html.H1('smartFolio'),
        html.Img(src='/assets/stocks.png')
    ], className='banner'),

    html.Div(children=[
        html.Br(),
        html.Label('Select your ticker'),
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

        html.Button('Submit', id='submit_button')
    
    ], style={'padding': 10, 'flex': 1, 'textAlign':'center'}),

    html.Div(id='selected_tickers', className='table'),    
    ],

    #html.Div(id = "teste",
    #children=[
    #    html.Br(),
    #    html.Label('Returns table'),
    #    table(returns)])],

    style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(
    Output('selected_tickers', 'children'),
    [Input('submit_button','n_clicks')],
    [State('tickers_dropdown', 'value'),
    State('start_date', 'value'),
    State('end_date', 'value'),
    State('intervals_dropdown', 'value')],
    prevent_initial_call=True
)
def get_some_prices(n, selected_tickers, start, end, interval):
    prices = yf.download(selected_tickers, start=start, end=end, interval=interval)['Adj Close'].fillna(0).reset_index()
    col = [{'name': i, 'id': i} for i in prices.columns]
    table = dash_table.DataTable(
            id='table',
            columns = col,
            page_size= 6,
            style_cell={'width': '45'},
            data = prices.to_dict('records')
    )
    return table

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
