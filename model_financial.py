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

def generate_wallets(returns, num_portfolios = 50000, risk_free = 0.000358):
    # vetores de dados
    portfolio_weights = []
    portfolio_exp_returns = []
    portfolio_vol = []
    portfolio_sharpe = []

    # média dos retornos
    returns.replace([np.inf, -np.inf], 0, inplace=True)
    mean_returns = returns.mean()

    # matriz de covariância 
    covariance = np.cov(returns[1:].T)

    for i in range(num_portfolios):
        # gerando pesos aleatórios
        k = np.random.rand(len(returns.columns))
        w = k / sum (k)

        # retorno
        R = np.dot(mean_returns, w)

        # risco
        vol = np.sqrt(np.dot(w.T, np.dot(covariance, w)))

        # sharpe ratio
        sharpe = (R - risk_free)/vol

        portfolio_weights.append(w)
        portfolio_exp_returns.append(R)
        portfolio_vol.append(vol)
        portfolio_sharpe.append(sharpe)

    wallets = {'weights': portfolio_weights,
              'returns': portfolio_exp_returns,
              'vol':portfolio_vol,
              'sharpe': portfolio_sharpe}

    return wallets

def best_porfolio(wallets: dict, method: str = 'sharpe_ratio') -> np.array:
    weights = wallets['weights']
    vol = wallets['vol']
    returns = wallets['returns']
    sharpe = wallets['sharpe']
    

    if method == 'sharpe_ratio':

        indice = np.array(sharpe).argmax()
        max_sharpe_return = returns[indice]
        max_sharpe_vol = vol[indice]
        max_sharpe = np.array([max_sharpe_return, max_sharpe_vol])

        return weights[indice], max_sharpe

    elif method == 'volatility':

        indice = np.array(vol).argmin()
        min_vol_return = returns[indice]
        min_vol_vol = vol[indice]
        min_vol = np.array([min_vol_return, min_vol_vol])

        return weights[indice], min_vol

    elif method == 'return': 

        indice = np.array(returns).argmax()
        max_return_return = returns[indice]
        max_return_vol = vol[indice]
        max_return = np.array([max_return_return, max_return_vol])
    
        return weights[indice], max_return
