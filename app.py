from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import plotly.express as px
import model_financial
import model_tickers
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
    Output('returns_fig', 'figure'),
    Output('weights_table', 'children'),
    Output('efficient_frontier', 'figure')],
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
    
    table_returns = view.table(returns)
    fig_returns = view.fig_line(returns, selected_tickers)

    wallets = model_financial.generate_wallets(returns.iloc[:, 1:])
    best_porfolio, max_sharpe = model_financial.best_porfolio(wallets)

    # Transform best_porfolio np.array into a pd.DataFrame
    best_porfolio = pd.DataFrame(data=best_porfolio, columns=['Pesos'], index=selected_tickers).reset_index()
    best_porfolio.columns = ['Ativos', 'Pesos']

    table_weights = view.table(best_porfolio)
    fig_wallets = view.plot_efficient_frontier(wallets, max_sharpe)

    return table_returns, fig_returns, table_weights, fig_wallets


if __name__ == '__main__':
    app.run_server(debug=True)