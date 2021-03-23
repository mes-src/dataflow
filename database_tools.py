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
    
    

