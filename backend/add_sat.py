import json
import psycopg2
from config import config


def add_satellite(name, norad_id, tle_line1, tle_line2):
    # Query to check if the satellite already exists
    fetch_satellite = "SELECT id FROM satellites WHERE norad_id = %s;"

    # Insert a new satellite
    insert_satellite = "INSERT INTO satellites (norad_id, name) VALUES (%s, %s) RETURNING id;"

    # Update an existing satellite
    update_satellite = "UPDATE satellites SET name = %s WHERE norad_id = %s;"

    # Insert or update TLE data
    assign_tle = """
        INSERT INTO tle_data (satellite_id, tle_line1, tle_line2)
        VALUES (%s, %s, %s)
        ON CONFLICT (satellite_id) DO UPDATE SET
        tle_line1 = EXCLUDED.tle_line1,
        tle_line2 = EXCLUDED.tle_line2;
    """

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Check if satellite already exists and get its ID
        cur.execute(fetch_satellite, (norad_id,))
        result = cur.fetchone()
        if result:
            satellite_id = result[0]
            # Update satellite name
            cur.execute(update_satellite, (name, norad_id))
        else:
            # Insert a new satellite and fetch its ID
            cur.execute(insert_satellite, (norad_id, name))
            satellite_id = cur.fetchone()[0]

        # Insert or update TLE data
        cur.execute(assign_tle, (satellite_id, tle_line1, tle_line2))

        # Commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

 
def upload_satellites_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        satellites_data = json.load(file)
        for satellite_name, tle_data in satellites_data.items():
            norad_id = extract_norad_id(tle_data[1])  # Extract NORAD ID from TLE line 2
            tle_line1 = tle_data[0]
            tle_line2 = tle_data[1]
            add_satellite(satellite_name, norad_id, tle_line1, tle_line2)

def extract_norad_id(tle_line2):
    # Extract the NORAD ID from the TLE line 2
    # Assuming the NORAD ID is the second field in the TLE line, separated by spaces
    return tle_line2.split()[1]

def main():
    json_file_path = 'satellites.json'
    upload_satellites_from_json(json_file_path)

if __name__ == "__main__":
    main()