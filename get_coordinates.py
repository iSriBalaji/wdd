import requests

def get_geolocation():
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        location = data['loc'].split(',')
        print(location[0],',', location[1])
        latitude = float(location[0])
        longitude = float(location[1])
        return latitude, longitude
    except requests.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None, None
    except (KeyError, ValueError) as e:
        print(f"Error parsing geolocation data: {e}")
        return None, None

latitude, longitude = get_geolocation()
if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Could not retrieve geolocation data.")
