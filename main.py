import scripts.apiRequests as apiRequests
import time
# Flask API URL (Running on the same Raspberry Pi)
BASE_URL = "http://127.0.0.1:5000"  # Change to Pi's IP if calling externally
#BASE_URL = "http://10.209.195.140:5000"  # Change to Pi's IP if calling externally

# Test the API with a GET request

while True:
    apiRequests.getAttendance()
    time.sleep(0.5)