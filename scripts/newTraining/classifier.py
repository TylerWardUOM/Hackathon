from modlib.models import COLOR_FORMAT, MODEL_TYPE, Model
from modlib.apps import Annotator
from modlib.devices import AiCamera
import numpy as np
import os
import cv2

ANNOTATIONS_PATH = "../annotations.txt"

class FaceClassifier:
    def __init__(self, model_file="imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk", model_type=MODEL_TYPE.RPK_PACKAGED):
        self.model = CustomModel()
        self.face_db = {}
        self.labels = self._load_annotations()

    def _load_annotations(self):
        """Load annotations from Sony's format"""
        annotations = {}
        with open(ANNOTATIONS_PATH) as f:
            for line in f:
                if line.startswith("#"): continue
                parts = line.strip().split(" | ")
                if len(parts) >= 2:
                    annotations[int(parts[0])] = parts[1]
        return annotations

    def build_database(self, faces_dir="../processed_faces"):
        """Extract features using Sony's optimized pipeline"""
        for person in os.listdir(faces_dir):
            embeddings = []
            for img_file in os.listdir(f"{faces_dir}/{person}"):
                img = cv2.imread(f"{faces_dir}/{person}/{img_file}")
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Use Sony's built-in feature extraction
                outputs = self.model.inference(img)
                if 'embedding' in outputs:
                    embeddings.append(outputs['embedding'])
            
            if embeddings:
                self.face_db[person] = np.mean(embeddings, axis=0)

    def recognize_face(self, frame):
        """Sony-optimized recognition pipeline"""
        outputs = self.model.inference(frame)
        if 'embedding' not in outputs:
            return []

        similarities = {
            name: self._cosine_similarity(outputs['embedding'], emb)
            for name, emb in self.face_db.items()
        }
        return [(name, score) for name, score in similarities.items() if score > 0.7]

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    #def post_processing(self, output_tensors):
#u	return pp_od_bscn(output_tensors)

# Initialize Sony components
device = AiCamera()
annotator = Annotator()
classifier = FaceClassifier()

# Build database (run once)
classifier.build_database()

# Real-time recognition loop
with device as stream:
    for frame in stream:
        # Convert frame to RGB (Sony models expect this format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get recognitions
        recognitions = classifier.recognize_face(rgb_frame)
        
        # Annotate and display
        for (name, score), detection in zip(recognitions, frame.detections):
            annotator.add_box(
                frame,
                detection.bbox,
                label=f"{name} ({score:.2f})",
                color=(0, 255, 0)
            )
        
        cv2.imshow("IMX500 Face Recognition", frame)
        if cv2.waitKey(1) == 27:  # ESC to exit
            break

device.release()
cv2.destroyAllWindows()
