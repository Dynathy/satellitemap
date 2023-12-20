import json
import psycopg2
from config import config

def connect():

    conn = None
    try:
        #read connection parameters from Config.py
        params = config()
        
        #connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        #create a Cursor
        cur = conn.cursor()
        
        #execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        
        #display the PostgreSQL database Server Version
        db_version = cur.fetchone()
        print(db_version)
        
        #close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database Connection Closed.')
                     
if __name__ == '__main__':
    connect()