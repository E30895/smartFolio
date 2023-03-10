import pandas as pd
import numpy as np

def risk_sigma2(returns: pd.DataFrame) -> pd.DataFrame:
    '''
    Calculate risk by standard deviation on pd.DataFrame
    and return dataframe of standard deviation.

    Arguments:
        DataFrame of returns
    '''
    vol = pd.DataFrame(np.std(returns))
    vol.columns = ["Risk STD"]
    
    return vol