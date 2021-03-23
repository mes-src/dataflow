'''
investment analysis data pipeline to populate & store psql db & local
with financaial statements, sec filings, and .xlsx templates for further anaysis

3.10.2021
@michael
'''
import re
import json
from io import StringIO
from bs4 import BeautifulSoup
import requests
import csv
import tkinter as tk
from tkinter import simpledialog
import yahoo_api_utils as yahooutils 
import pandas as pd 
import numpy as np 
import database_tools as dbtools
import sys, os 
import ui as gui
from sqlalchemy import create_engine

class Company:



	def __init__(self, ticker):
		self.ticker = ticker
		self.extracted_dict = dict()
		self.get_yahoo_profile()


	def get_yahoo_profile(self):
		print('profile')


	def get_yahoo_financial_statements(self):
		#Financial Statements
		response = yahooutils.build_financial_statements_urls(self.ticker)
		soup = BeautifulSoup(response.text, 'html.parser')
		data_dict = yahooutils.parse_financial_statements_json_response(soup)

		extracted_dict = dict() # parse json response from yahoo api
		for kk,vv in data_dict.items(): #keys = xdict returned from util.parse_json()
			parsed_statements = []
			for s in vv:
				statement = {}
				for k,v in s.items(): # line items from statements
					try:
						statement[k] = v['raw']
					except TypeError:
						continue
					except KeyError:
						continue
					parsed_statements.append(statement)
			extracted_dict[kk] = parsed_statements

		self.extracted_dict = extracted_dict
		return self

	def download_financial_statements_to_local(self):
		import sys, os 		
		for k,v in self.extracted_dict.items(): # for each k = sheet type, v = []
			localdir = os.getcwd() + '/output/' +  str(self.ticker) + '/' 
			if not os.path.isdir(localdir):
				os.mkdir(localdir)
			
			localp = f'{localdir}{self.ticker}_{k}.csv'
			with open(localp, 'w') as csv_file:  
				writer = csv.writer(csv_file)
				for kk,vv in v[0].items():
					writer.writerow([kk, vv])
		print('download successfull for ' + str(self.extracted_dict.keys()))


	def upload_financial_statements_to_db(self, upload_type='all'):
		cwd  = os.getcwd() + '/'
		conn, creds = dbtools.connect(cwd)

		if upload_type == 'all':
			statements_abrev_names = ['qbs','qis','qcf', 'abs','ais','acf']
			for sheet_type in statements_abrev_names:
				table_name = f'{self.ticker}_{sheet_type}'
				csv_path = cwd + 'output/{}/{}.csv'.format(self.ticker, table_name)
				df = pd.read_csv(csv_path, header = None)
				print(df.head())  # sql alchemy
				engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(creds.get('user'),creds.get('pass'),creds.get('host'), creds.get('db')))
				uri = 'postgres+psycopg2://{}:{}@{}:5432/{}'.format(creds.get('user'),creds.get('pass'),creds.get('host'),creds.get('db'))
				if not engine.dialect.has_table(engine, table_name): # if table !exist, create it
					df.to_sql(table_name, uri)
				else: 
					df.to_sql(table_name, uri, if_exists='replace')
		else:
			pass




	def __str__(self,):
		return self.ticker

 

def init():

	runtime_vars = gui.build_gui()
	tickers, local_download, db_update = runtime_vars.get('tickers'), runtime_vars.get('locald'), runtime_vars.get('updb')
	print([tickers, local_download, db_update])
 
	if "," in tickers:
		items = tickers.split(",")
		for item  in items:
			c = Company(item.strip().upper()).get_yahoo_financial_statements()
			if local_download == 'True':
				c.download_financial_statements_to_local() 
	else:
		c = Company(tickers.strip().upper()).get_yahoo_financial_statements()
		if local_download == 'True':
			c.download_financial_statements_to_local()
		if db_update == 'True':
			c.upload_financial_statements_to_db()


if __name__ == '__main__':
	init()

