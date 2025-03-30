from modlib.apps import Annotator, BYTETracker
from modlib.devices import AiCamera
from modlib.models.zoo import SSDMobileNetV2FPNLite320x320
import threading
from datetime import datetime

class CameraProcessor:
    def __init__(self, config, tracker_args, database, attendance_tracker):
        self.device = AiCamera()
        self.model = SSDMobileNetV2FPNLite320x320()
        self.device.deploy(self.model)
        self.tracker = BYTETracker(tracker_args)
        self.annotator = Annotator(thickness=1, text_thickness=1, text_scale=0.4)
        self.database = database
        self.attendance_tracker = attendance_tracker
        self.config = config
        self._running = False

    def _process_frame(self, frame):
        detections = frame.detections[frame.detections.confidence > self.config.CONFIDENCE_THRESHOLD]
        detections = detections[detections.class_id == self.config.TARGET_CLASS_ID]
        detections = self.tracker.update(frame, detections)
        
        current_time = datetime.now()
        for detection in detections:
            track_id = detection[3]
            self.attendance_tracker.add_detection(track_id, current_time)
        
        labels = [f"#{t} {self.model.labels[c]}: {s:0.2f}" for _, s, c, t in detections]
        self.annotator.annotate_boxes(frame, detections, labels=labels)
        frame.display()

    def start(self):
        self._running = True
        threading.Thread(target=self._run).start()

    def _run(self):
        with self.device as stream:
            for frame in stream:
                if not self._running:
                    break
                self._process_frame(frame)

    def stop(self):
        self._running = False
