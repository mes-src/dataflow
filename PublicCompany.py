import pandas as pd
import numpy as np 
import datetime
import os
from pandas_datareader import data as web
from yahoo_fin.stock_info import *
import yfinance as yfin
from utils import yahoo_api_utils as yahooutils
import re
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
now = datetime.now()
import sys, os  
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine
import requests
import csv
cwd = os.getcwd()




class Company():
    '''
    @ michael 3/23/11

    a collection of methods to pull and parse stock price data for compannies

    '''

    def __init__(self, ticker):
        self.ticker = ticker
        self.extracted_dict = dict()

    def dt_tools(self):
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

    def get_daterangee():
        date_rng = pd.date_range(start='1/1/2018', end='1/08/2018', freq='H')
        timestamp_date_rng = pd.to_datetime(date_rng, infer_datetime_format=True)

    
    def get_solo(self):
        start = '2014'
        end = datetime(2017, 5, 24)
        df = web.DataReader(self.ticker, 'yahoo', start=start, end=end)
        #df.info()
        return df

    
    def get_cbind_onloop(self, plot = False):
        tickers_list = ['AMZN','GOOGL', 'NVDA', 'MLM', 'ATO', 'KMI','JNJ', 'JPM', 'C']
        df = yfin.download(tickers_list,'2015-1-1')['Adj Close']
        print(df.head())
        def _plot():
            import matplotlib.pyplot as plt 
            ((df.pct_change()+1).cumprod()).plot(figsize=(10, 7))

            plt.legend()
            plt.title("Returns", fontsize=16)
            plt.ylabel('Cumulative Returns', fontsize=14)
            plt.xlabel('Year', fontsize=14)
            plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)

            plt.show()
        if plot == True:
            _plot()
    
        return df


    def write_csv_onloop(self):
        tickers = [ 'BABA', 'TSLA', 'NVDA', 'EEM', 'AAPL', 'C', 'BAC', 'MELI']
        data_source = 'yahoo'
        start_date = '20201121'
        end_date = '20210112'
        for _ticker in tickers:
            df = web.DataReader(_ticker, data_source, start_date, end_date)
            p = f'{cwd}/output/individuals/{_ticker}.csv'
            df.to_csv(p)
    



    def get_yahoo_financial_statements(self, download = False, upload = False):
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


        def download_financial_statements_to_local(self):
            for k,v in self.extracted_dict.items(): # for each k = sheet type, v = []
                localdir = f'{os.getcwd()}/output/yahoo_fundamentals/{self.ticker}/'  
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
        
        if download == True:
            download_financial_statements_to_local(self)
        elif upload == True:
            upload_financial_statements_to_db(self)


    def get_quote_table(self, indexvalues, nItems):
        frames = []
        indexnames = []
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
        df = pd.concat(frames, axis = 1).transpose()
        df.columns = ['1yrTargetEst','52weekRange','Ask','AvgVol','Beta','Bid','DayRange','EPS','EarningsDate','ExDiv','DivYield','MktCap','Open','PE','Close','Quote','Volume']
        print(df.head())
        outp = './output/quote_table.csv'
        df.to_csv(outp)

        print()
        print('Errors: ' + str(errorlist))
        return df


        
    def __str__(self):
        pass







## Usage ##

c = Company('AAPL')
tickers = ['AAPL', 'TSLA']

#c.get_solo()
c.write_csv_onloop()
c.get_cbind_onloop(plot = True)
c.get_quote_table(tickers, len(tickers))


for _t in tickers:
    print(f'...processing for {_t}...')
    Company(_t).get_yahoo_financial_statements(download = True, upload = False)


