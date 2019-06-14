import requests
import json
import time

url = "https://api.samsara.com/v1/fleet/locations"
YOUR_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
querystring = {"access_token": YOUR_ACCESS_TOKEN}
response = requests.request("GET", url, params=querystring)
print("--- all vehicles ---")
print(json.dumps(response.json(), indent=2))
print()

response_json = response.json()
list_of_vehicles = response_json["vehicles"]
first_vehicle = list_of_vehicles[0]
vehicle_id = first_vehicle["id"]

now = int(time.time() * 1000)
then = now - 15000

url = f"https://api.samsara.com/v1/fleet/vehicles/{vehicle_id}/locations"
querystring = {"access_token": YOUR_ACCESS_TOKEN, "startMs": str(then), "endMs": str(now)}
response = requests.request("GET", url, params=querystring)
print("--- single vehicle locations ---")
print(json.dumps(response.json(), indent=2))
print()
