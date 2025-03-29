from modlib.models import CustomModel
from modlib.data import FeatureExtractor
from modlib.apps import Annotator
from modlib.devices import AiCamera
import numpy as np
import os

ANNOTATIONS_PATH = "../annotations.txt" 

class FaceClassifier(CustomModel):
    def __init__(self, model_path="imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"):
        super().__init__(model_path)
        self.feature_extractor = FeatureExtractor()
        self.face_db = {}  # {name: embedding}
        
    def build_database(self, faces_dir="faces"):
        """Extract features from training images"""
        for person in os.listdir(faces_dir):
            embeddings = []
            for img_path in os.listdir(f"{faces_dir}/{person}"):
                frame = self.load_image(f"{faces_dir}/{person}/{img_path}")
                detections = self.inference(frame)
                if detections:
                    face_roi = detections[0].crop(frame)  # Largest face
                    emb = self.feature_extractor(face_roi)
                    embeddings.append(emb)
            if embeddings:
                self.face_db[person] = np.mean(embeddings, axis=0)
                
    def post_processing(self, outputs):
        """Custom face matching"""
        face_emb = outputs['embeddings']
        similarities = {
            name: self.cosine_similarity(face_emb, db_emb)
            for name, db_emb in self.face_db.items()
        }
        return max(similarities, key=similarities.get)

    def add_person(self, name, images):
        embeddings = [self.feature_extractor(img) for img in images]
        self.face_db[name] = np.mean(embeddings, axis=0)


# Initialize
device = AiCamera()
model = FaceClassifier()
model.build_database() 
device.deploy(model)

annotator = Annotator()

# Real-time recognition
with device as stream:
    for frame in stream:
        detections = frame.detections[frame.detections.confidence > 0.55]
        
        # Get custom classifications
        labels = [model.post_processing(d.output) for d in detections]
        
        # Annotate
        annotator.annotate_boxes(frame, detections, labels=labels)
        frame.display()

