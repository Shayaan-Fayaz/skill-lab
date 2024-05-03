import requests
import json

# Define the ESP32 IP address and port
esp32_ip = "192.168.223.174"
esp32_port = 80

# Define the URL for the detection endpoint
url = f"http://{esp32_ip}:{esp32_port}/detect"

classes = set()
classes.add("headphones")
classes.add("phones")
classes.add("usb")

# Define the JSON payload
payload = {
    "classes": list(classes),
    "count": 5
}

# Convert payload to JSON string
payload_json = json.dumps(payload)

# Set the Content-Type header to application/json
headers = {'Content-Type': 'application/json'}

# Send POST request to ESP32 API
response = requests.post(url, data=payload_json, headers=headers)
# response = requests.get(url)
# Print response
print("Response:")
print(response.status_code)
print(response.text)

#
# classes = set()
#
# classes.add("head")
# classes.add("nose")
# classes.add("head")
# print(list(classes))