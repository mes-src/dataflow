from pandas_datareader import data
import pandas as pd
import numpy as np
import datetime

now = datetime.datetime.now()


def retrieve_historical_data(timespan, tickers, outputpath):
	tickers = [ 'BABA', 'TSLA', 'NVDA', 'EEM', 'AAPL', 'C', 'BAC', 'MELI']
	#tickers = ['AMAT', 'AMD', 'LRCX', 'HD', 'JNJ', 'WYN', 'LVS', 'CRM']

	year = now.year
	month = now.month
	day = now.day
	hour = now.hour
	minute = now.minute

	data_source = 'yahoo'
	start_date = str(year - 1) + '-' + str(month) + '-' + str(day)
	end_date = str(year) + '-' + str(month) + '-' + str(day)


	for item in tickers:
		print(item),
		panel_data = data.DataReader(item, data_source, start_date, end_date)
		path = outputpath + item + timespan + '.csv'
		panel_data.to_csv(path)

		
