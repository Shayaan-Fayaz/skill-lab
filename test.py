import requests

url = "http://192.168.94.174/json"
response = requests.get(url)
print(response.json())