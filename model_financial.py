import pandas as pd
import numpy as np
import yfinance as yf

"""
Esse módulo executa cálculos financeiros
"""


def get_tickers() -> list:
    ''' Get many brazilians stock tickers from a text file and
        return a list.
    '''
    my_file = open("tickers_list.txt", "r")
    data = my_file.read()
    tickers_list = data.split("\n")
    my_file.close()

    return tickers_list


def log_return(price_series: pd.DataFrame) -> pd.DataFrame:
    '''
    This function calculate log-returns of stock DataFrame and with "np.log()"
    and return on pandas.Series.
    
    Arguments:
        price_series: a pd.DataFrame dtype float64
    '''
    log_returns = np.log(price_series).diff().fillna(0)
    return_cumreturn = log_returns.cumsum()
    return log_returns, return_cumreturn

def markowitz():
    pass