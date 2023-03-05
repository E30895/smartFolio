import pandas as pd

def na_replace(data: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    '''
    This function replaces every NaN in the pd.Series or pd. Dataframe
    with the number 0.

    Parameters:

        data: pd.DataFrame or pd.Series
            A pd.Series or a pd.DataFrame to remove the NaN.
    
    '''
    
    data_without_na = data.fillna(0)

    return data_without_na


def replaces(data: pd.Series) -> pd.Series:
    pass
