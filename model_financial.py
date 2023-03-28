import pandas as pd
import numpy as np

"""
Esse módulo executa cálculos financeiros
"""

def log_return(price_series: pd.DataFrame) -> pd.DataFrame:
    '''
    This function calculate log-returns of stock DataFrame and with "np.log()"
    and return on pandas.Series.
    
    Arguments:
        price_series: a pd.DataFrame dtype float64
    '''
    log_returns = np.log(price_series).diff().fillna(0)
    log_returns.reset_index(inplace = True)
    return log_returns

def markowitz():
    pass
