import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from skyfield.api import load, EarthSatellite
from config import config  # Ensure you have a config file with DB details

app = Flask(__name__)
CORS(app)

def connect_to_db():
    params = config()  # Load database configuration parameters
    return psycopg2.connect(**params)

def get_satellite_data_from_db():
    conn = connect_to_db()
    satellite_data = []

    with conn.cursor() as cur:
        # Assuming your table has columns 'name', 'norad_id', 'tle_line1', 'tle_line2'
        cur.execute("""
            SELECT s.name, s.norad_id, t.tle_line1, t.tle_line2
            FROM satellites s
            JOIN tle_data t ON s.id = t.satellite_id;
        """)
        rows = cur.fetchall()

        for row in rows:
            name, norad_id, tle1, tle2 = row
            # Process the data as required
            satellite_data.append({
                "name": name,
                "norad_id": norad_id,
                "tle1": tle1,
                "tle2": tle2
                # Add other fields if necessary
            })

    conn.close()
    return satellite_data

def calculate_position(tle1, tle2):
    ts = load.timescale()
    satellite = EarthSatellite(tle1, tle2)
    time = ts.now()
    geocentric = satellite.at(time)
    subpoint = geocentric.subpoint()
    return subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m
    
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
    
@app.route('/get_satellite_data')
def get_satellite_data():
    satellites = get_satellite_data_from_db()
    satellite_data = []
    
    for sat in satellites:
        lat, lon, alt = calculate_position(sat['tle1'], sat['tle2'])
        path = calculate_satellite_path(sat['tle1'], sat['tle2'])
        
        satellite_data.append({
            "name": sat['name'],
            "latitude": lat,
            "longitude": lon,
            "altitude": alt,
            "path": path
        })
        
    return jsonify(satellite_data)

if __name__ == '__main__':
    app.run(debug=True)
