'''
postgresSQL db on awsrds
'''

import configparser
import psycopg2

def read_ini(cwd):
    CONFIG_PATH = cwd + 'database.ini'  
    CONFIG = configparser.RawConfigParser()
    CONFIG.read(CONFIG_PATH, encoding='utf-8-sig') # "utf-8" for UTF-8 without BOM

    PSQL_HOST = CONFIG.get('postgresql', 'host')
    PSQL_DB = CONFIG.get('postgresql', 'database')
    PSQL_USER = CONFIG.get('postgresql', 'user')
    PSQL_PASS = CONFIG.get('postgresql', 'password')

    creds = {'host':PSQL_HOST, 'db':PSQL_DB, 'user':PSQL_USER, 'pass':PSQL_PASS}
    return creds


def connect(cwd):
    creds = read_ini(cwd)

    try:  
        conn = psycopg2.connect(
        host=creds.get('host'),
        database=creds.get('db'),
        user=creds.get('user'),
        password=creds.get('pass')
        )

        print('postgresql connection succesfull')
        return (conn, creds)

    except Exception as e:
        print(e)
    
    

def upload_financial_statements_to_db(self, upload_type='all'):
    """
    populate sql database with financial statment items feed from yahoo api parser

    """
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


