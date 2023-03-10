import yfinance as yf
import pandas as pd
import tabula


def get_tickers() -> list:
    ''' Get many brazilians stock tickers from a text file and
        return a list.
    '''
    my_file = open("tickers_list.txt", "r")
    data = my_file.read()
    tickers_list = data.split("\n")
    my_file.close()

    return tickers_list


def get_prices(tickers: str | list, start: str, end: str, interval: str) -> pd.Series | pd.DataFrame:
    '''
    This function download the prices of a list of tickers and return 
    a pandas.Series (if the "tickers" parameter is a string) 
    or a pandas.DataFrame (if the "tickers" parameter is a list of strings)
    with the adjusted close prices of each ticker, replacing all NaN with 0.

    Parameters:
        tickers : list
            List of tickers to download
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
    '''
    
    prices = yf.download(tickers, start, end, interval)['Adj Close'].fillna(0)

    return prices
