# paths
from pathlib import Path
import sys, os

# data
import pandas as pd 
import numpy as np
p = f'{Path(os.getcwd()).parent.absolute()}/'
sys.path.append(p)
TICKER = 'TSLA'
TICKER_LIST = ['GOOGL', 'AMZN']
import CompanyData as co 
import Fundamentals as fun 


# co.get_yahoo_financial_statements(TICKER_LIST, download = False)

def read_fundamentals(ticker):
    frames = []
    try:
        for sheet_type in co.statements_abrev_names:
            path = f'{p}output/yahoo_fundamentals/{ticker}/{ticker}_{sheet_type}.csv'
            df = pd.read_csv(path, names =['LineItems','Value'])
            frames.append(df)
        return frames
    except Exception as e:
        print(f' error fundamental file does not exist for {ticker}_{sheet_type} ')
        return None


q_bs,q_is,q_cf,a_bs,a_is,a_cf  = read_fundamentals(TICKER)


def extract_line_item(df, line_item_text):
    try:
        x = df.loc[df['LineItems'] == line_item_text].Value.values[0]
        return x
    except Exception as e:
        return 0


# -- #
def cash_flow_analysis():
    print(a_cf.LineItems.values)
    ffo = extract_line_item(a_cf, 'totalCashFromOperatingActivities')
    capex = extract_line_item(a_cf, 'capitalExpenditures')
    div = extract_line_item(a_cf, 'dividendsPaid')
    depr = extract_line_item(a_cf, 'depreciation')
    ni = extract_line_item(a_cf, 'netIncome')

    ''' retained cash flow '''
    rcp = (ffo+depr) - capex - div
    print('RCP: {:,}'.format(rcp))

    ''' payout ratio '''
    por = div / ni
    print('Payout Ratio: {:,}'.format(por))
    
    def forecast_fcf_growth():
        pass

    
cash_flow_analysis()
