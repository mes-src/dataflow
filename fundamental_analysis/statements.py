# paths
from pathlib import Path
import sys, os

# data
import pandas as pd 
import numpy as np
p = f'{Path(os.getcwd()).parent.absolute()}/'
sys.path.append(p)


import CompanyData as co 

# co.get_yahoo_financial_statements(['GOOGL', 'AMZN'], download = False)

def read_fundamentals(ticker, sheet_type):
    try:
        path = f'{p}output/yahoo_fundamentals/{ticker}/{ticker}_{sheet_type}.csv'
        df = pd.read_csv(path, names =['LineItems','Value'])
        # df = df.set_index('LineItem')
        return df
    except Exception as e:
        print(f' error fundamental file does not exist for {ticker}_{sheet_type} ')
    
cf = read_fundamentals('GOOGL', 'acf')
print(cf.LineItems.values)


def extract_line_item(df, line_item_text):
    try:
        x = df.loc[df['LineItems'] == line_item_text].Value.values[0]
        return x
    except Exception as e:
        # print(e)
        return 0


ffo = extract_line_item(cf, 'totalCashFromOperatingActivities')
capex = extract_line_item(cf, 'capitalExpenditures')
div = extract_line_item(cf, 'dividends')

rcp = ffo - capex - div
print('RCP: {:,}'.format(rcp))


