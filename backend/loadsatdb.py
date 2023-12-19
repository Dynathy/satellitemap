# -*- coding: utf-8 -*-
import psycopg2
import requests
from datetime import datetime, timedelta
import os
import json

# Database connection parameters
DB_NAME = "satdata"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5004"

# Celestrak URL
CELESTRAK_URL = "https://www.celestrak.com/NORAD/elements/visual.txt"

# File to store the timestamp of the last update
LAST_UPDATE_FILE = "last_update.json"

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def fetch_tle_data():
    try:
        response = requests.get(CELESTRAK_URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching TLE data: {e}")
        return None

def can_fetch_data():
    if not os.path.exists(LAST_UPDATE_FILE):
        return True
    
    with open(LAST_UPDATE_FILE, "r") as file:
        data = json.load(file)
        last_update = datetime.fromisoformat(data["last_update"])
        if datetime.now() - last_update > timedelta(hours=3):
            return True

    return False

def save_last_update_time():
    with open(LAST_UPDATE_FILE, "w") as file:
        data = {"last_update": datetime.now().isoformat()}
        json.dump(data, file)
        
def extract_norad_id(tle_line1):
    """
    Extracts the NORAD ID from the first line of TLE data.

    The NORAD ID is a sequence of five digits starting from the 3rd to the 7th character in the TLE line 1.
    """
    try:
        norad_id = int(tle_line1[2:7])
        return norad_id
    except ValueError:
        print(f"Error extracting NORAD ID from: {tle_line1}")
        return None

def ensure_satellite_exists(conn, norad_id, name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM satellites WHERE norad_id = %s", (norad_id,))
        result = cur.fetchone()
        if not result:
            cur.execute("INSERT INTO satellites (norad_id, name) VALUES (%s, %s)", (norad_id, name))
            conn.commit()
       
def process_and_insert_tle_data(conn, tle_data):
    lines = tle_data.strip().split("\n")
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        tle1 = lines[i + 1].strip()
        tle2 = lines[i + 2].strip()
        norad_id = extract_norad_id(tle1)  # Extract NORAD ID from TLE line 1

        if norad_id is not None:
            ensure_satellite_exists(conn, norad_id, name)
            insert_tle_data(conn, norad_id, tle1, tle2, datetime.now())

def insert_tle_data(conn, norad_id, tle_line1, tle_line2, epoch):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tle_data (satellite_id, tle_line1, tle_line2, epoch)
                VALUES (%s, %s, %s, %s)
                """, (norad_id, tle_line1, tle_line2, epoch)
            )
            conn.commit()
    except Exception as e:
        print(f"Error inserting TLE data: {e}")
        conn.rollback()
        
def main():
    if can_fetch_data():
        tle_data = fetch_tle_data()
        if tle_data:
            conn = connect_to_db()
            if conn:
                process_and_insert_tle_data(conn, tle_data)
                conn.close()
            save_last_update_time()
        else:
            print("Failed to fetch TLE data.")
    else:
        print("Recently updated. Next update available in less than 3 hours.")

if __name__ == "__main__":
    main()
