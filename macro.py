

import pandas as pd 

import pandas_datareader as pdr
# load gold data from FRED API & save copy locally to CSV file
series = ['GOLDAMGBD228NLBM']
gold_download = pdr.data.DataReader(series, 
                                    'fred', 
                                    start='1968-12-31')
# convert daily to annual
gold_download = gold_download.resample('A').last().reset_index()
gold_download.set_index(pd.DatetimeIndex(gold_download['DATE']).year, inplace=True)
gold_download['return'] = gold_download['GOLDAMGBD228NLBM'].pct_change()
gold_download.to_csv('gold_fred.csv')



series = ['GDPCA']

gdp_download = pdr.data.DataReader(series, 
                                   'fred', 
                                   start='1926-12-31')
gdp_download.reset_index(inplace=True)
gdp_download.set_index(pd.DatetimeIndex(gdp_download['DATE']).year, inplace=True)
gdp_download['GDP'] = gdp_download['GDPCA'].pct_change()
# https://fortunly.com/statistics/us-gdp-by-year-guide/#gref
gdp_download.loc[1928, 'GDP'] = 0.0110
gdp_download.loc[1929, 'GDP'] = 0.0652
gdp_download.to_csv('gdp_fred.csv')

print(gdp_download)





data_xls = 'http://www.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls'
data_sheet = "Returns by year"
# these will change as rows get added on Damodaran website
skiprows = range(17)
skipfooter = 10
download_df = pd.read_excel('http://www.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls', 
                         sheet_name=data_sheet, 
                         skiprows=skiprows,
                         skipfooter=skipfooter)
download_df = download_df.set_index('Year')
data_df = download_df.copy()
data_df = data_df.rename(columns = {'Inflation Rate': 'CPI',
           'S&P 500 (includes dividends)2': 'S&P',
           '3-month T. Bill (Real)': 'T-Bills',
           '!0-year T.Bonds': 'T-Notes',
           'Baa Corp Bonds': 'Baa Corps',
          })[['CPI', 'S&P', 'T-Bills', 'T-Notes', 'Baa Corps']]
data_df["GDP"] = gdp_download['GDP']
data_df["Gold"] = longrun_data['gold'] - data_df['CPI']
# reorder
data_df = data_df[['GDP', 'CPI', 'S&P', 'T-Bills', 'T-Notes', 'Baa Corps', 'Gold']]


#https://github.com/druce/portfolio_optimization/blob/master/Portfolio%20optimization.ipynb