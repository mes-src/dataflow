from yahoo_fin.stock_info import *
import pandas as pd 
import numpy as np 


frames = []
indexnames = []

def scrape_yahoo_finance(indexvalues, nItems):
	for ticker in indexvalues[:nItems]:
		print(str(ticker), sep='', end='  |  ', flush=True)
		errorlist = []
		try:
			quotedata = get_quote_table(ticker , dict_result = True)
			df = pd.DataFrame(list(quotedata.items()),columns = ['names',ticker])
			indexnames = df['names']
			df = df[ticker]
			frames.append(df)
		except Exception as e:
			errorlist.append(ticker)
	print()
	print('Errors: ' + str(errorlist))
	return frames



def init(df):
	print('YahooFin | Scrape Yahoo Finance Data')
	print('Scrape Tickers Process')
	indexvalues = df.index.values
	nItems =len(indexvalues)
	#nItems = 6

	print('Numbr of Tickers to loop: ' + str(nItems))
	xframes = scrape_yahoo_finance(indexvalues, nItems)
	df = pd.concat(xframes, axis = 1).transpose()

	df.columns = ['1yrTargetEst','52weekRange','Ask','AvgVol','Beta','Bid','DayRange','EPS','EarningsDate','ExDiv','DivYield','MktCap','Open','PE','Close','Quote','Volume']

	outp = './output/SPACyahooPrices.csv'
	df.to_csv(outp)
	return df


