from skyfield.api import Topos, load
from datetime import datetime

def create_satellite(tle1, tle2):
    # Load the TLE data into a satellite object
    satellites = load.tle_file('http://celestrak.com/NORAD/elements/stations.txt')
    satellite = satellites[0]
    return satellite

def get_current_position(satellite):
    # Use the current time
    ts = load.timescale()
    time = ts.now()

    # Calculate the satellite's position at the current time
    geocentric = satellite.at(time)

    # Get the geographic position (lat, long, alt)
    subpoint = geocentric.subpoint()
    return subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m

# TLE data for a satellite
tle1 = '1 25544U 98067A   21010.91667824  .00001264  00000-0  35036-4 0  9992'
tle2 = '2 25544  51.6441 161.3405 0001728  15.3450 344.8204 15.48915117265678'

# Create the satellite object
satellite = create_satellite(tle1, tle2)

# Get the current position
latitude, longitude, altitude = get_current_position(satellite)
print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} m")
