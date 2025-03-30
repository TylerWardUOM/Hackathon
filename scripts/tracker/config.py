class BYTETrackerArgs:
    track_thresh: float = 0.25
    track_buffer: int = 30
    match_thresh: float = 0.8
    aspect_ratio_thresh: float = 3.0
    min_box_area: float = 1.0
    mot20: bool = False

class AppConfig:
    MIN_ATTENDANCE_DURATION = 300  # 5 minutes in seconds
    TRACK_TIMEOUT = 30  # Seconds before considering a track inactive
    CONFIDENCE_THRESHOLD = 0.55
    TARGET_CLASS_ID = 0  # Person class ID
