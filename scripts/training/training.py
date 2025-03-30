import os
from deepface import DeepFace
import pickle
from tqdm import tqdm  # Import tqdm for progress bars

# Path to the user image database
user_images_path = "../data"
user_embeddings = {}

# Iterate through all folders with progress bar
for user_folder in tqdm(os.listdir(user_images_path), desc="Processing users"):
    user_folder_path = os.path.join(user_images_path, user_folder)
    
    if os.path.isdir(user_folder_path):
        user_name = user_folder
        embeddings = []
        
        # Get list of images and create progress bar for images
        image_files = [f for f in os.listdir(user_folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        image_progress = tqdm(image_files, desc=f"Processing {user_name}'s images", leave=False)
        
        # Process each image in the user's folder
        for image in image_progress:
            img_path = os.path.join(user_folder_path, image)
            try:
                # Update progress bar description with current image
                image_progress.set_postfix({"current": image[:15] + "..." if len(image) > 15 else image})
                
                # Extract embeddings using SFace model
                result = DeepFace.represent(
                    img_path=img_path,
                    model_name="SFace",
                    enforce_detection=False
                )
                embeddings.append(result[0]["embedding"])
                
            except Exception as e:
                print(f"\nError processing image {img_path}: {e}")
                continue

        # Store the embeddings for the user
        user_embeddings[user_name] = embeddings

# Save the embeddings dictionary to a file
with open("user_embeddings.pkl", "wb") as f:
    pickle.dump(user_embeddings, f)

print("\nEmbeddings saved to user_embeddings.pkl")
