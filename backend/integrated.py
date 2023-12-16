import json
import os
import atexit
import signal
from datetime import datetime, timedelta
import requests
from skyfield.api import EarthSatellite, load
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

satellite_data = []  # Define it as a global variable

def save_data_on_shutdown():
    # Assuming 'satellite_data' is the data you want to save
    # and 'save_data_with_timestamp' is your function to save data to a JSON file
    global satellite_data
    save_data_with_timestamp(satellite_data, 'satellite_data.json')
    print("Data saved on shutdown.")
    
# Function to fetch TLE data
def fetch_tle_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return response.text

# Function to parse TLE data
def parse_tle_data(raw_data):
    lines = raw_data.strip().split('\n')
    satellites = {}
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        tle1 = lines[i+1].strip()
        tle2 = lines[i+2].strip()
        satellites[name] = (tle1, tle2)
    return satellites

# Function to calculate satellite position
def calculate_position(tle1, tle2):
    ts = load.timescale()
    satellite = EarthSatellite(tle1, tle2)
    time = ts.now()
    geocentric = satellite.at(time)
    subpoint = geocentric.subpoint()
    return subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m
    
# Corrected calculate_satellite_path function
def calculate_satellite_path(tle1, tle2, duration_hours=4, interval_minutes=15):
    ts = load.timescale()
    satellite = EarthSatellite(tle1, tle2)
    path = []
    now = ts.now()
    for minutes in range(0, duration_hours * 60, interval_minutes):
        future_time = ts.tt_jd(now.tt + minutes / 1440)  # Correct way to advance time
        geocentric = satellite.at(future_time)
        subpoint = geocentric.subpoint()
        path.append([subpoint.longitude.degrees, subpoint.latitude.degrees, subpoint.elevation.m])
    return path
    
# Function to save data with timestamp
def save_data_with_timestamp(data, filename='satellite_data.json'):
    with open(filename, 'w') as file:
        json.dump({'last_updated': datetime.now().isoformat(), 'data': data}, file)

# Function to load data if it's recent
def load_recent_data(filename='satellite_data.json', max_age_hours=3):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            cached_data = json.load(file)
            last_updated = datetime.fromisoformat(cached_data['last_updated'])
            if datetime.now() - last_updated < timedelta(hours=max_age_hours):
                return cached_data['data']
    return None

def signal_handler(signum, frame):
    save_data_on_shutdown()
    exit(0)
    
atexit.register(save_data_on_shutdown)
signal.signal(signal.SIGINT, signal_handler)

# Main function
@app.route('/get_satellite_data')
def get_satellite_data():
    cached_data = load_recent_data()
    if cached_data:
        return jsonify(cached_data)

    url = 'https://www.celestrak.com/NORAD/elements/visual.txt'
    raw_data = fetch_tle_data(url)
    satellites = parse_tle_data(raw_data)

    satellite_data = []
    for name, (tle1, tle2) in satellites.items():
        lat, lon, alt = calculate_position(tle1, tle2)
        path = calculate_satellite_path(tle1, tle2)
        satellite_data.append({
            "name": name,
            "latitude": lat,
            "longitude": lon,
            "altitude": alt,
            "path": path
        })

    save_data_with_timestamp(satellite_data)
    return jsonify(satellite_data)

if __name__ == '__main__':
    app.run(debug=True)
