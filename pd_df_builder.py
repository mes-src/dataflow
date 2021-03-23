# build initial df using pandas_datareader
# date range



#qunadl, tiingo, pandas_datareader

import yahoo_fin as yf 

import pandas_datareader.data as web
import pandas as pd
from datetime import datetime
import numpy as np
date_rng = pd.date_range(start='1/1/2018', end='1/08/2018', freq='H')


timestamp_date_rng = pd.to_datetime(date_rng, infer_datetime_format=True)

# Import the yfinance. If you get module not found error the run !pip install yfinance from your Jupyter notebook
import yfinance as yf
import matplotlib.pyplot as plt



def multi_stock():
	tickers_list = ['AMZN','GOOGL', 'NVDA', 'MLM', 'ATO', 'KMI','JNJ', 'JPM', 'C']
	data = yf.download(tickers_list,'2015-1-1')['Adj Close']
	print(data.head())

	def plot():
		((data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
		plt.legend()
		plt.title("Returns", fontsize=16)
		plt.ylabel('Cumulative Returns', fontsize=14)
		plt.xlabel('Year', fontsize=14)
		plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
		plt.show()
	#plot()
	return data

df = multi_stock()





from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage

mu = mean_historical_return(df)
S = CovarianceShrinkage(df).ledoit_wolf()
'''
mu will then be a pandas series of estimated expected returns for each asset,
and S will be the estimated covariance matrix (part of it is shown below):
'''
print(mu)
print(S)

from pypfopt.efficient_frontier import EfficientFrontier
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
print(ef)
print(weights)

x = ef.portfolio_performance(verbose=True)
print(x)

cleaned_weights = ef.clean_weights()
ef.save_weights_to_file("weights.txt")  # saves to file

# shorting initiate with negative bounds
#ef = EfficientFrontier(mu, S, weight_bounds=(-1,1))
# market neutral
# ef.efficient_return(target_return=0.2, market_neutral=True)

# incentivize optimizer to choose different weights
ef = EfficientFrontier(mu, S)
# ef.add_objective(objective_functions.L2_reg, gamma=0.1)
w = ef.max_sharpe()
print(ef.clean_weights())

# quantities to buy for allocation
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
latest_prices = get_latest_prices(df)
da = DiscreteAllocation(w, latest_prices, total_portfolio_value=20000)
allocation, leftover = da.lp_portfolio()
print(allocation)


