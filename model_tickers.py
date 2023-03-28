import requests

def get_tickers() -> list:
    ''' Get many brazilians stock tickers from a text file and
        return a list.
    '''
    url = 'https://github.com/E30895/smartFolio/raw/main/tickers_list.txt'
    request = requests.get(url)
    tickers_list = request.text.split()
    request.close()

    return tickers_list
