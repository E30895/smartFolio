import pandas as pd
import numpy as np

#Devolver uma matriz de retornos
def log_return(price_series: pd.DataFrame) -> pd.DataFrame:
    '''
    This function calculate log-returns of stock DataFrame and with "np.log()"
    and return on pandas.Series.
    
    Arguments:
        price_series: a pd.DataFrame dtype float64
    '''
    log_returns = np.log(price_series).diff().fillna(0).reset_index()
    return_cumreturn = log_returns.cumsum().reset_index()
    return log_returns, return_cumreturn
