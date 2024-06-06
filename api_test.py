# client.py (Python script to send request)
import requests

# URL of the FastAPI endpoint
url = "http://0.0.0.0:8081/device/all"  # Replace <Linux_Server_IP> with your actual server IP or domain

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpc3JpYmFsYWppIiwiaWQiOjQsInJvbGUiOjEsImV4cCI6MTcxNzIwNzcwOH0.qo5Xl6HcRsEjSbD1--LLWyfE_JL2mDkQtVL-gWFrgFs'

headers = {
            "Authorization": f"Bearer {token}"
        }

# Send GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Failed to get response. Status code: {response.status_code}")
