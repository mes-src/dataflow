import pandas_datareader.data as web

securities = {'BAMLCC0A0CMTRIV'   : 'US Corp Master TRI',
              'BAMLHYH0A0HYM2TRIV': 'US High Yield TRI',
              'BAMLEMCBPITRIV'    : 'Emerging Markets Corporate Plus TRI',
              'GOLDAMGBD228NLBM'  : 'Gold (London, USD)',
              'DGS10'             : '10-Year Treasury CMR',
              }

df = web.DataReader(name=list(securities.keys()), data_source='fred', start=2000)
df = df.rename(columns=securities).dropna(how='all').resample('B').mean()
print(df)