import requests

BASE_URL = "http://127.0.0.1:5000"  # Change to Pi's IP if calling externally

def attend_student(name):
    data = {"studentName": name}
    response = requests.post(f"{BASE_URL}/attend", json=data)
    print("Response from /attend:", response.json())

def getStatus():
    response = requests.get(f"{BASE_URL}/status")
    print("Response from /status:", response.json())

def getAttendance(lectureName):
    data = {"lectureName": lectureName}
    response = requests.post(f"{BASE_URL}/attendance", json=data)
    print("Response from /attendance:", response.json())

def verifyStudent():
    data = {"studentName": "Tyler"}
    response = requests.post(f"{BASE_URL}/verify", json=data)
    print("Response from /verify:", response.json())