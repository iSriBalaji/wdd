import requests

url = 'http://0.0.0.0:8081/auth/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': '',
    'username': 'isribalaji',
    'password': 'lenovo',
    'scope': '',
    'client_id': '',
    'client_secret': ''
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 201:
    token = response.json().get('access_token')
    print(f"Access token: {token}")
else:
    print(f"Failed to get token: {response.status_code}, {response.text}")
