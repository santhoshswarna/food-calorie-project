import tensorflow as tf
import numpy as np
from PIL import Image
import io

model = tf.keras.models.load_model(
    "food_classifier_densenet201.h5",
    compile=False
)

IMG_SIZE = (224, 224)

def predict_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    preds = model.predict(image)
    return int(np.argmax(preds)), float(np.max(preds))
