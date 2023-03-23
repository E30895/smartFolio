import datetime
import re
import yfinance as yf
import pandas as pd


def get_tickers() -> list:
    ''' Get many brazilians stock tickers from a text file and
        return a list.
    '''
    my_file = open("tickers_list.txt", "r")
    data = my_file.read()
    tickers_list = data.split("\n")
    my_file.close()

    return tickers_list


def get_prices(selected_tickers: list, start: str, end: str, interval: str) -> pd.DataFrame:
    '''
    This function download the prices of a list of tickers and return 
    a pandas.Series (if the "tickers" parameter is a string) 
    or a pandas.DataFrame (if the "tickers" parameter is a list of strings)
    with the adjusted close prices of each ticker, replacing all NaN with 0.

    Parameters:
        tickers : list
            List of tickers to download
        start: str
            Download start date string (YYYY-MM-DD).
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD).
            Default is now
        interval : str
            Valid intervals: 1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
    '''
    
    start_splitted = list(map(int, re.split('-', start, 2)))
    end_splitted = list(map(int, re.split('-', end, 2)))
    
    start_date = str(int(datetime.datetime(start_splitted[0], start_splitted[1], start_splitted[2], 21).timestamp()))
    end_date = str(int(datetime.datetime(end_splitted[0], end_splitted[1], end_splitted[2], 21).timestamp()))

    if len(selected_tickers) == 1:
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{selected_tickers}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
        prices = pd.read_csv(url)[['Date', 'Adj Close']].astype({'Date': 'string'})
    else:
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{selected_tickers[0]}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
        prices = pd.read_csv(url)['Date'].astype('string')
        
        for ticker in selected_tickers:
            url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
            ticker_prices = pd.read_csv(url)[['Date', 'Adj Close']].astype({'Date': 'string'})
            prices = pd.merge(prices, ticker_prices, how='outer', on='Date')
    
    
    prices.columns = ['Date'] + selected_tickers

    return prices
