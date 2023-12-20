import psycopg2
from config import config

import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE satellites (
            id SERIAL PRIMARY KEY,
            norad_id INT UNIQUE NOT NULL,
            name VARCHAR(255)
        )
        """,
        """ 
        CREATE TABLE tle_data (
            id SERIAL PRIMARY KEY,
            satellite_id INT REFERENCES satellites(id),
            tle_line1 TEXT,
            tle_line2 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )   
        """,
        """
        CREATE TABLE historical_tle_data (
            id SERIAL PRIMARY KEY,
            satellite_id INT REFERENCES satellites(id),
            tle_line1 TEXT,
            tle_line2 TEXT,
            epoch TIMESTAMP,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()