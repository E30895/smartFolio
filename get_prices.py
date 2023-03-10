import yfinance as yf
import pandas as pd
import tabula


def get_tickers() -> list:
    
    tables = tabula.read_pdf('Brazilian_Stock_Exchange_Companies.pdf', pages='1-11')
    
    for table in tables:
        for coluna in table.columns:
            if 'Name Symbol' in coluna:
                table['Name Symbol'+'.SA'] = table['Name Symbol']
            if '.SA' not in coluna:
                table.drop(columns=coluna, inplace=True)
    
    for table in tables:
        table.dropna(inplace=True)

    tickers_list = []

    for table in tables:
        for i in range(len(table)):
            tickers_list.append(table.iloc[i,0][-8:])

    for table in tables:
        for name in table.columns.values:
            if name[-8:-3].isupper():
                tickers_list.append(name[-8:-3])

    for ticker in tickers_list:
        if ' ' in ticker:
            tickers_list.remove(ticker)

    for ticker in tickers_list:
        if '.SA' not in ticker:
            tickers_list.remove(ticker)

    for ticker in tickers_list:
        if ticker.startswith('X'):
            tickers_list.remove(ticker)

    tickers_list

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