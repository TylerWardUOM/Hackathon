import requests

# Flask API URL (Running on the same Raspberry Pi)
BASE_URL = "http://127.0.0.1:5000"  # Change to Pi's IP if calling externally
#BASE_URL = "http://10.209.195.140:5000"  # Change to Pi's IP if calling externally

# Test the API with a GET request
response = requests.get(f"{BASE_URL}/status")
print("Response from /status:", response.json())

# Send data using a POST request
data = {"studentName": "Tyler"}
response = requests.post(f"{BASE_URL}/attend", json=data)
print("Response from /attend:", response.json())


response = requests.get(f"{BASE_URL}/attendance")
print("Response from /attendance:", response.json())

data = {"studentName": "Tyler"}
response = requests.post(f"{BASE_URL}/verify", json=data)
print("Response from /verify:", response.json())

response = requests.get(f"{BASE_URL}/attendance")
print("Response from /attendance:", response.json())
