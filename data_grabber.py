import requests
import json

# URL of the API
api_url = "https://east.albion-online-data.com/"

# Query parameters
item_list = "T4_BAG,T5_BAG"
locations = "Caerleon,Bridgewatch"
qualities = "2"

# Construct the full URL
url = f"{api_url}api/v2/stats/prices/{item_list}?locations={locations}&qualities={qualities}"

print(url)

# Send a GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Pretty-print JSON data
    print(json.dumps(data, indent=4, sort_keys=True))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
