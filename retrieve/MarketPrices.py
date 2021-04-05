import numpy as np
import pandas as pd 
import quandl

def get_solo(self):
    start = '2014'
    end = datetime(2017, 5, 24)
    df = web.DataReader(self.ticker, 'yahoo', start=start, end=end)
    #df.info()
    return df

def get_quandl(self):
    symbol = 'FB.US'
    quandl = web.DataReader(symbol, 'quandl', '2015-01-01')
    quandl.info()

def get_tiingo(self):
    df = web.get_data_tiingo('GOOG', api_key=os.getenv('TIINGO_API_KEY'))


def get_cbind_onloop(plot = False):
    """
    Download yahoo finance for an array of tickers and column bind them into
    a singl dataframe --> (Format to pass directly into PyPortfolioOpt)

    :return: historical price time series for array of tickers 
    :rtype: pd.dataframe
    """
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
    """
    Output csv files of historical time sries data for array of tickers

    :param w: 
    :type w: 
    :param obj: 
    :type obj: 
    :return: 
    :rtype: 
    """
    tickers = [ 'BABA', 'TSLA', 'NVDA', 'EEM', 'AAPL', 'C', 'BAC', 'MELI']
    data_source = 'yahoo'
    start_date = '20201121'
    end_date = '20210112'
    for _ticker in tickers:
        df = web.DataReader(_ticker, data_source, start_date, end_date)
        p = f'{cwd}/output/individuals/{_ticker}.csv'
        df.to_csv(p)


    def dt_tools(self):
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

    def get_daterange():
        """
        Build a range of dates between two days to use as indx

        :param w: 
        :type w: 
        :param obj: 
        :type obj: 
        :return: 
        :rtype: 
        """
        date_rng = pd.date_range(start='1/1/2018', end='1/08/2018', freq='H')
        timestamp_date_rng = pd.to_datetime(date_rng, infer_datetime_format=True)

   


    def get_quote_table(self, indexvalues, nItems):
        """
        Pars yahoo api via json urls to retrieve financial statement data
        
        :param w: 
        :type w: 
        :param obj: 
        :type obj: 
        :return: 
        :rtype: 
        """
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
    
    def get_book_data(self):
        """
        retrieve full order book data from IEX which includes bid/ask spreads
        
        :param w: 
        :type w: 
        :param obj: 
        :type obj: 
        :return: 
        :rtype: df
        """
        book = web.get_iex_book(self.ticker)
        list(book.keys())
        print(book)
        orders = pd.concat([pd.DataFrame(book[side]).assign(side=side) for side in ['bids', 'asks']])
        print(orders.head())
        for key in book.keys():
            try:
                print(f'\n{key}')
                print(pd.DataFrame(book[key]))
            except:
                print(book[key])
        pd.DataFrame(book['trades']).head()
    