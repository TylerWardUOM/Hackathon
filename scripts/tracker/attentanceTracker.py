from threading import Lock
from collections import deque, defaultdict
from datetime import datetime, timedelta

class AttendanceTracker:
    def __init__(self, config):
        self.track_queue = deque()
        self.active_tracks = defaultdict(lambda: {
            'start': None,
            'last_seen': None,
            'student_name': None,
            'lecture': None,
            'confirmed': False
        })
        self.lock = Lock()
        self.config = config

    def add_detection(self, track_id, timestamp):
        with self.lock:
            if track_id not in self.active_tracks:
                self.track_queue.append(track_id)
            if not self.active_tracks[track_id]['start']:
                self.active_tracks[track_id]['start'] = timestamp
            self.active_tracks[track_id]['last_seen'] = timestamp

    def get_pending_tracks(self):
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

    def check_completed(self):
        completed = []
        with self.lock:
            now = datetime.now()
            for tid, data in list(self.active_tracks.items()):
                if data['student_name'] and (now - data['last_seen']).seconds > self.config.TRACK_TIMEOUT:
                    duration = (data['last_seen'] - data['start']).seconds
                    if duration >= self.config.MIN_ATTENDANCE_DURATION:
                        completed.append({
                            'student': data['student_name'],
                            'lecture': data['lecture'],
                            'duration': duration
                        })
                    del self.active_tracks[tid]
        return completed
