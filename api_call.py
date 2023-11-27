import requests
import json

# Define the URL of your Flask API endpoint
url = "https://azureweb.ngrok.app/api/payrun"

# Define the JSON data to send in the request body

data = {
    "operation":"message_processed",
    "runId":"6538ecdb40f9b7395d468639",
    "email":"rohanricky3@gmail.com"
    }

    # Set the headers to indicate JSON content
headers = {
        'Content-Type': 'application/json'
    }
try:
        # Send the POST request with JSON data
    response = requests.post(url, data=json.dumps(data), headers=headers)

        # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("API request successful")
        print("Response:", response.text)
    else:
        print("API request failed with status code:", response.status_code)
        print("Response:", response.text)

except Exception as e:
    print("An error occurred:", str(e))

#runid and email