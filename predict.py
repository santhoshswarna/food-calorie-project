import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import gdown

# -----------------------------
# Model Configuration
# -----------------------------
MODEL_PATH = "food_classifier_densenet201.h5"

# 🔴 Replace with YOUR Google Drive File ID
FILE_ID = "1VRO8kCSTdJ8tQ0pkrps-VicXLen8YzCN"

DOWNLOAD_URL = f"https://drive.google.com/uc?id=1VRO8kCSTdJ8tQ0pkrps-VicXLen8YzCN"

# -----------------------------
# Download model if not present
# -----------------------------
if not os.path.exists(MODEL_PATH):
    print("Downloading ML model from Google Drive...")
    gdown.download(DOWNLOAD_URL, MODEL_PATH, quiet=False)
    print("Model download completed.")

# -----------------------------
# Load Model
# -----------------------------
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
print("Model loaded successfully.")

# -----------------------------
# Image Settings
# -----------------------------
IMG_SIZE = (224, 224)

# -----------------------------
# Prediction Function
# -----------------------------
def predict_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)

    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    preds = model.predict(image)
    
    class_index = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return class_index, confidence
