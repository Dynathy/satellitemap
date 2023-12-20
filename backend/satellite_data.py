import requests
import json
import os
from datetime import datetime, timedelta

LAST_CALL_FILE = "last_api_call.txt"
JSON_FILE_PATH = "satellites.json"

def fetch_tle_data(url):
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the fetch fails
    return response.text

def parse_tle_data(raw_data):
    lines = raw_data.strip().split('\n')
    satellites = {}
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        tle1 = lines[i+1].strip()
        tle2 = lines[i+2].strip()
        satellites[name] = (tle1, tle2)
    return satellites

def save_data_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def can_fetch_data():
    if not os.path.exists(LAST_CALL_FILE):
        return True

    with open(LAST_CALL_FILE, 'r') as file:
        last_call_time = datetime.fromisoformat(file.read().strip())

    return datetime.now() - last_call_time > timedelta(hours=3)

def update_last_call_time():
    with open(LAST_CALL_FILE, 'w') as file:
        file.write(datetime.now().isoformat())

def main():
    if can_fetch_data():
        url = 'https://www.celestrak.com/NORAD/elements/visual.txt'
        raw_data = fetch_tle_data(url)
        satellites = parse_tle_data(raw_data)
        save_data_to_json(satellites, JSON_FILE_PATH)
        update_last_call_time()
        print("Data fetched and saved.")
    else:
        print("Data was recently fetched. Skipping API call.")

if __name__ == "__main__":
    main()

