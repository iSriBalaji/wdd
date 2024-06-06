import requests

# URL of the FastAPI token endpoint
auth_url = "http://0.0.0.0:8081/auth/token"  # Replace with your actual server IP or domain

# Credentials for authentication
username = "isribalaji"
password = "lenovo"

# Data payload for the token request
auth_data = {
    "grant_type": "",
    "username": username,
    "password": password,
    "scope": "",
    "client_id": "",
    "client_secret": ""
}

# Headers for the token request
auth_headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Send POST request to obtain the token
auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

# Check if the authentication request was successful
if auth_response.status_code == 201:
    # Extract the token from the JSON response
    token = auth_response.json().get("access_token")
    print("TOKEN", token)
    if token:
        # URL of the FastAPI endpoint you want to access
        api_url = "http://0.0.0.0:8081/device/all"  # Replace with your actual server IP or domain

        # Headers with the token for authentication
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Send GET request with the token
        api_response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if api_response.status_code == 200:
            # Print the JSON response
            print(api_response.json())
        else:
            print(f"Failed to get response from {api_url}. Status code: {api_response.status_code}")
    else:
        print("Failed to obtain token.")
else:
    print(f"Failed to authenticate. Status code: {auth_response.status_code}")
