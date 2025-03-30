from flask import Flask, jsonify, request
from Database import Database
from flask_cors import CORS  # Import CORS
from threading import Lock, Thread
from collections import deque, defaultdict
from datetime import datetime, timedelta
import time

database=Database()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ---
class AttendanceTracker:
    def __init__(self):
        self.track_queue = deque()
        self.active_tracks = defaultdict(lambda: {
            'start': None,
            'last_seen': None,
            'student_name': None,
            'lecture': None
        })
        self.lock = Lock()
        self.min_duration = timedelta(minutes=5)  # 5 minute threshold

    def add_detection(self, track_id):
        with self.lock:
            now = datetime.now()
            if track_id not in self.active_tracks:
                self.track_queue.append(track_id)
                self.active_tracks[track_id]['start'] = now
            self.active_tracks[track_id]['last_seen'] = now

    def get_pending(self):
        with self.lock:
            return [tid for tid in self.track_queue if not self.active_tracks[tid]['student_name']]

    def assign_student(self, track_id, student_name, lecture_name):
        with self.lock:
            if track_id in self.active_tracks:
                self.active_tracks[track_id]['student_name'] = student_name
                self.active_tracks[track_id]['lecture'] = lecture_name
                try:
                    self.track_queue.remove(track_id)
                except ValueError:
                    pass

    def check_attendance(self):
        completed = []
        with self.lock:
            now = datetime.now()
            for tid, data in list(self.active_tracks.items()):
                if data['student_name'] and (now - data['last_seen']).seconds > 30:
                    duration = data['last_seen'] - data['start']
                    if duration >= self.min_duration:
                        completed.append({
                            'student': data['student_name'],
                            'lecture': data['lecture'],
                            'duration': duration.total_seconds()
                        })
                    del self.active_tracks[tid]
        return completed

# Initialize tracker
attendance_tracker = AttendanceTracker()
# ---
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

@app.route('/assign', methods=['POST'])
def assign_track():
    data = request.json
    if not all(k in data for k in ["track_id", "student_name", "lecture_name"]):
        return jsonify({"error": "Missing parameters"}), 400
    
    attendance_tracker.assign_student(
        data["track_id"],
        data["student_name"],
        data["lecture_name"]
    )
    return jsonify({"success": True})

def process_attendance():
    while True:
        time.sleep(30)
        completed = attendance_tracker.check_attendance()
        for record in completed:
            # Use existing database interface
            database.attendStudent(record['student'])  
            # Add duration tracking if supported
            if hasattr(database, 'record_duration'):
                database.record_duration(
                    record['student'],
                    record['lecture'],
                    record['duration']
                )

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
                attendance_tracker.add_detection(track_id)
            labels = [f"#{t} {model.labels[c]}: {s:0.2f}" for _, s, c, t in detections]
            annotator.annotate_boxes(frame, detections, labels=labels)

            frame.display()


if __name__ == '__main__':
    # Start background services
    Thread(target=process_attendance, daemon=True).start()
    Thread(target=camera_loop, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000)
