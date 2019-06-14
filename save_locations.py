import requests
import json
import time
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, MetaData

### Call Samsara API ###
url = "https://api.samsara.com/v1/fleet/vehicles/locations"
YOUR_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

now = int(time.time() * 1000)
then = now - 15000

querystring = {"access_token": YOUR_ACCESS_TOKEN, "startMs": str(then), "endMs": str(now)}
response = requests.request("GET", url, params=querystring).json()

### Write to database
engine = create_engine('sqlite:///locations.db')
metadata = MetaData()
locations = Table('locations', metadata,
    Column('vehicle_id', Integer, primary_key=True),
    Column('latitude', Numeric),
    Column('location', String),
    Column('longitude', Numeric),
    Column('speedMilesPerHour', Numeric),
    Column('timeMs', Integer, primary_key=True),
    Column('name', String)
)
metadata.create_all(engine)

con = engine.connect()
for vehicle in response:
    vehicle_id = vehicle['id']
    vehicle_name = vehicle['name']
    vehicle_locations = vehicle['locations']
    for location in vehicle_locations:
        con.execute(locations.insert(),
            vehicle_id = vehicle_id,
            latitude = location['latitude'],
            location = location['location'],
            longitude = location['longitude'],
            speedMilesPerHour = location['speedMilesPerHour'],
            timeMs = location['timeMs'],
            name = vehicle_name
        )