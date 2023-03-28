import requests
import re
import datetime

def get_tickers() -> list:
    ''' Get many brazilians stock tickers from a text file and
        return a list.
    '''
    url = 'https://github.com/E30895/smartFolio/raw/main/tickers_list.txt'
    request = requests.get(url)
    tickers_list = request.text.split()
    request.close()

    return tickers_list


def get_prices(tickers: list, start: str, end: str, interval: str) -> pd.DataFrame:
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
    start_splitted = list(map(int, re.split('-', start, 2)))
    end_splitted = list(map(int, re.split('-', end, 2)))
    
    start_date = str(int(datetime.datetime(start_splitted[0], start_splitted[1], start_splitted[2], 21).timestamp()))
    end_date = str(int(datetime.datetime(end_splitted[0], end_splitted[1], end_splitted[2], 21).timestamp()))

    if len(tickers) == 1:
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{tickers}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
        prices = pd.read_csv(url)[['Date', 'Adj Close']].astype({'Date': 'string'})
    else:
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{tickers[0]}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
        prices = pd.read_csv(url)['Date'].astype('string')
        for ticker in tickers:
            url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
            ticker_prices = pd.read_csv(url)[['Date', 'Adj Close']].astype({'Date': 'string'})
            prices = pd.merge(prices, ticker_prices, how='outer', on='Date')
    
    prices.columns = ['Date'] + tickers
    
    prices = prices.set_index('Date')

    return prices
