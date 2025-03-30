from flask import Flask, jsonify, request
from Database import Database
from flask_cors import CORS  # Import CORS
from threading import Lock, Thread
from collections import deque, defaultdict
from datetime import datetime, timedelta
import time
from apiRequests import *

database=Database()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class AttendanceTracker():

    def __init__(self):
        self.seenId = []
        self.currentAttendants = []

    def process_attendance(self, user_id):
        if user_id not in self.seenId:
            name = database.getNext()
            if name != None:
                self.currentAttendants.append((name, datetime.now()))

    def check_attendance(self):
        attended = []
        for name, allotted_time in self.currentAttendants:
            if allotted_time + 300 > datetime.now():
                attended.append(name)
                self.currentAttendants.remove((name, allotted_time))
        return attended

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Running", "device": "Raspberry Pi"})

# Example: Receive data via POST request
@app.route('/attend', methods=['POST'])
def attend():
    data = request.json  # Get Student Name from request
    
    if not data or "studentName" not in data:
        return jsonify({"error": "Missing 'studentName' in request"}), 400

    database.attendStudent(data["studentName"])
    return jsonify({"Marked as Attended": data["studentName"]})

@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.json  # Get Student Name from request
    if not data or "lectureName" not in data:
        return jsonify({"error": "Missing 'lectureName' in request"}), 400
    return jsonify({"attended": database.getStudents(data["lectureName"])})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json  # Get Student Name from request
    
    if not data or "studentName" not in data:
        return jsonify({"error": "Missing 'studentName' in request"}), 400

    database.verifyStudent(data["studentName"])
    return jsonify({"Marked as Verified": data["studentName"]})

def multipleVer(input_arr):
    for name in input_arr:
        database.verifyStudent(name)


attendance_tracker = AttendanceTracker()

def camera_loop():
    from modlib.apps import Annotator, BYTETracker
    from modlib.devices import AiCamera
    from modlib.models.zoo import SSDMobileNetV2FPNLite320x320

    class BYTETrackerArgs:
        track_thresh: float = 0.25
        track_buffer: int = 30
        match_thresh: float = 0.8
        aspect_ratio_thresh: float = 3.0
        min_box_area: float = 1.0
        mot20: bool = False

    device = AiCamera()
    model = SSDMobileNetV2FPNLite320x320()
    device.deploy(model)
    tracker = BYTETracker(BYTETrackerArgs())
    annotator = Annotator(thickness=1, text_thickness=1, text_scale=0.4)


    with device as stream:
        for frame in stream:
            detections = frame.detections[frame.detections.confidence > 0.55]
            detections = detections[detections.class_id == 0]
            detections = tracker.update(frame, detections)
            
            for detection in detections:
                track_id = detection[3]
                attendance_tracker.process_attendance(track_id)
                tracker.add_detection(track_id)
            labels = [f"#{t} {model.labels[c]}: {s:0.2f}" for _, s, c, t in detections]
            annotator.annotate_boxes(frame, detections, labels=labels)

            frame.display()

def process_loop():
    while True:
        time.sleep(30)
        to_add = attendance_tracker.check_attendance()
        multipleVer(to_add)

if __name__ == '__main__':
    # Start background services
    Thread(target=process_loop, daemon=True).start()
    Thread(target=camera_loop, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000)
