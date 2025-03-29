from axpi import runtime, camera
import numpy as np
import cv2
import time
import os

# Initialize Sony SDK
runtime.initialize("imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk")
camera.init()

# Custom face database (name: embedding)
face_db = {}

# Configuration
DETECTION_THRESH = 0.7  # Face detection confidence
RECOG_THRESH = 0.85     # Recognition similarity
TRACKING_BUFFER = 15    # Seconds after disappearance

# Time tracking dictionary {name: [first_seen, last_seen]}
presence = {}

def extract_face_embedding(face_roi):
    """Convert face ROI to embedding using Sony's model"""
    # Preprocess for SSD MobileNetV2
    blob = cv2.dnn.blobFromImage(
        face_roi, 
        scalefactor=1/127.5, 
        size=(320, 320), 
        mean=[127.5, 127.5, 127.5],
        swapRB=True
    )
    
    # Run through Sony's model
    outputs = runtime.inference(blob)
    
    # Extract final embedding (modify based on model output)
    return outputs[0]['feature_vector']  # Verify output layer name

def build_database():
    for person in os.listdir("faces"):
        person_path = os.path.join("faces", person)
        embeddings = []
        
        for img_file in os.listdir(person_path):
            img = cv2.imread(os.path.join(person_path, img_file))
            
            # Detect largest face
            detections = runtime.inference(img)
            faces = [d for d in detections if d['confidence'] > DETECTION_THRESH]
            if faces:
                main_face = max(faces, key=lambda x: x['width']*x['height'])
                x,y,w,h = main_face['bbox']
                face_roi = img[y:y+h, x:x+w]
                
                # Extract and store embedding
                embeddings.append(extract_face_embedding(face_roi))
        
        # Average embeddings for person
        if embeddings:
            face_db[person] = np.mean(embeddings, axis=0)
    
    # Save database
    np.savez("face_db.npz", **face_db)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def update_presence(name):
    now = time.time()
    if name in presence:
        presence[name][1] = now  # Update last seen
    else:
        presence[name] = [now, now]  # First appearance

def check_presence():
    current_names = list(presence.keys())
    now = time.time()
    
    for name in current_names:
        if now - presence[name][1] > TRACKING_BUFFER:
            duration = presence[name][1] - presence[name][0]
            print(f"{name}: {duration:.1f} seconds")
            del presence[name]

def main():
    # Load or build database
    try:
        face_db = dict(np.load("face_db.npz", allow_pickle=True))
    except FileNotFoundError:
        build_database()
    
    while True:
        frame = camera.capture()
        detections = runtime.inference(frame)
        
        for det in detections:
            if det['confidence'] > DETECTION_THRESH:
                x,y,w,h = det['bbox']
                face_roi = frame[y:y+h, x:x+w]
                
                # Get embedding
                emb = extract_face_embedding(face_roi)
                
                # Compare with database
                similarities = {
                    name: cosine_similarity(emb, db_emb)
                    for name, db_emb in face_db.items()
                }
                
                if similarities:
                    best_match = max(similarities, key=similarities.get)
                    if similarities[best_match] > RECOG_THRESH:
                        update_presence(best_match)
                        cv2.putText(frame, best_match, (x,y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                        
        check_presence()
        cv2.imshow("Sony Face Recognition", frame)
        
        if cv2.waitKey(1) == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

# Set before runtime.initialize()
runtime.set_config({
    'npu': {
        'core_number': 2,
        'frequency': 800  # This could be 
    },
    'camera': {
        'resolution': (1280, 720),
        'fps': 20
    },
    'memory': {
        'allocation_priority': 'high_performance'
    }
})
