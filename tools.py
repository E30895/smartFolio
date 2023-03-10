import pandas as pd
import numpy as np

def line (data: pd.Series):
   pass

def histogram (data: pd.Series):
   pass
  
def scatterplot(data: pd.Series):
   pass

def table(data: pd.DataFrame, max_rows=10):
   #data.sort_values(by=date, ascending= False)
   return html.Table([
        
        #CABEÇALHOS
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        
        #CORPO
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])