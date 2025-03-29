import requests

# Flask API URL (Running on the same Raspberry Pi)
BASE_URL = "http://127.0.0.1:5000"  # Change to Pi's IP if calling externally

# Test the API with a GET request
response = requests.get(f"{BASE_URL}/status")
print("Response from /status:", response.json())

# Send data using a POST request
data = {"studentName": "Alice", "temperature": 36.5}
response = requests.post(f"{BASE_URL}/data", json=data)
print("Response from /data:", response.json())
