from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import plotly.express as px
import model_financial
import model_econometrics
import view

"""
Esse módulo é o main, chamando todos os outros módulos
"""

# Cria o controlador da aplicação
app = Dash(__name__)

tickers = model_tickers.get_tickers()
intervals = ['1d','5d','1wk','1mo','3mo']


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
def main(n_clicks, selected_tickers, start, end, interval):
    prices = model_tickers.get_prices(selected_tickers, start=start, end=end, interval=interval)
    returns = model_financial.log_return(prices)
    table = view.table(returns)
    fig = view.fig_line(returns, selected_tickers)
    return table, fig


if __name__ == '__main__':
    app.run_server(debug=True)
