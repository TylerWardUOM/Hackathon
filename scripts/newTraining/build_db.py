from axpi import runtime, camera
import numpy as np
import os
import cv2

runtime.initialize("imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk")
camera.init()

face_db = {}

for person in os.listdir("../faces"):
    person_path = os.path.join("../faces", person)
    embeddings = []
    
    for img_file in os.listdir(person_path):
        img_path = os.path.join(person_path, img_file)
        frame = camera.load_still(img_path)
        detections = runtime.inference(frame)
        
        if detections:
            main_face = max(detections, key=lambda x: x['confidence'])
            x,y,w,h = main_face['bbox']
            face_roi = frame[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (320, 320))
            emb = runtime.extract_features(face_roi)
            embeddings.append(emb)
    
    if embeddings:
        face_db[person] = np.mean(embeddings, axis=0)

np.savez("face_db.npz", **face_db)
print("Database built with", len(face_db), "people")
