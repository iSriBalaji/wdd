import requests

def get_geolocation():
    try:
        response = requests.get('http://ip-api.com/json/')
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        if data['status'] == 'success':
            print(data['lat'],',', data['lon'])
            latitude = data['lat']
            longitude = data['lon']
            return latitude, longitude
        else:
            print("Error fetching geolocation data.")
            return None, None
    except requests.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None, None

latitude, longitude = get_geolocation()
if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Could not retrieve geolocation data.")
