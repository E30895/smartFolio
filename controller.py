from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import model_financial
import model_econometrics
import view

"""
Esse módulo é o main, chamando todos os outros módulos
"""

# Cria o controlador da aplicaç~ao
app = Dash(__name__)

tickers = model_financial.get_tickers()
intervals = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']

layout = view.layout_creator(tickers= tickers, intervals= intervals)
app.layout = layout


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