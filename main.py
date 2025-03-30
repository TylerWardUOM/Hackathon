import scripts.apiRequests as apiRequests
import time
# Flask API URL (Running on the same Raspberry Pi)
BASE_URL = "http://127.0.0.1:5000"  # Change to Pi's IP if calling externally
#BASE_URL = "http://10.209.195.140:5000"  # Change to Pi's IP if calling externally

# Test the API with a GET request


apiRequests.attend_student("Tyler")
apiRequests.attend_student("Harrison")
apiRequests.attend_student("Jamie")
apiRequests.attend_student("Conor")
time.sleep(0.2)