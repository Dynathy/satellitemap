import requests

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

def main():
    url = 'https://www.celestrak.com/NORAD/elements/visual.txt'
    raw_data = fetch_tle_data(url)
    satellites = parse_tle_data(raw_data)
    
    # Displaying the first 5 satellites
    for name, tle in list(satellites.items())[:5]:
        print(f"Satellite: {name}\nTLE Line 1: {tle[0]}\nTLE Line 2: {tle[1]}\n")

if __name__ == "__main__":
    main()

