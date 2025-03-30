import cv2
import numpy as np
import pickle
from deepface import DeepFace

# Load the precomputed user embeddings from the saved file
with open("user_embeddings.pkl", "rb") as f:
    user_embeddings = pickle.load(f)

model_name = "SFace"

# Function to compute embedding for a given image
def get_embedding(image):
    try:
        result = DeepFace.represent(img_path=image, model_name=model_name, enforce_detection=False)
        return result[0]["embedding"]
    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return None

# Function to calculate the similarity between two embeddings
def compare_embeddings(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))

cap = cv2.VideoCapture(0)# dont know if this is correct

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save the frame as a temporary image
    temp_img = "temp.jpg"
    cv2.imwrite(temp_img, frame)

    # Extract the face embedding from the current image
    current_embedding = get_embedding(temp_img)
    if current_embedding is None:
        continue

    # Find the best match for the current embedding
    best_match = None
    lowest_distance = float('inf')

    for user_name, embeddings in user_embeddings.items():
        for user_embedding in embeddings:
            distance = compare_embeddings(current_embedding, user_embedding)
            if distance < lowest_distance:
                best_match = user_name
                lowest_distance = distance

    # Annotate the frame with the best match result
    if best_match is not None and lowest_distance < 0.6:  # Threshold to determine a match
        text = f"Hello, {best_match}!"
        color = (0, 255, 0)  # Green for match
    else:
        text = "Unknown"
        color = (0, 0, 255)  # Red for no match

    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Show the frame
    cv2.imshow("Face Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
