from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import yfinance as yf
import get_data
import plotly.express as px


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

@app.callback(
    [Output('selected_tickers', 'children'),
    Output('grafico', 'figure')],
    [Input('submit_button','n_clicks')],
    [State('tickers_dropdown', 'value'),
    State('start_date', 'value'),
    State('end_date', 'value'),
    State('intervals_dropdown', 'value')],
    prevent_initial_call=True
)
def get_some_prices(n, selected_tickers, start, end, interval):
    prices = yf.download(selected_tickers, start=start, end=end, interval=interval)['Adj Close'].fillna(0)
    prices2 = prices.reset_index()
    col = [{'name': i, 'id': i} for i in prices2.columns]
        
    table = dash_table.DataTable(
            id='table',
            columns = col,
            page_size= 6,
            style_cell={'width': '45'},
            data = prices2.to_dict('records')
            )
    
    log_returns = np.log(prices).diff().fillna(0).reset_index()
    return_cumreturn = log_returns.cumsum()

    fig = px.line(log_returns, x='Date', y=selected_tickers)

    return table, fig


if __name__ == '__main__':
    app.run_server(debug=True)
