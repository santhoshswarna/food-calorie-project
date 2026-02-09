import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load model (.h5)
model = load_model("food_classifier_densenet201.h5", compile=False)

# Load CSV and fit label encoder on food labels
df = pd.read_csv("food_labels.csv")
label_encoder = LabelEncoder()
label_encoder.fit(df["label"].values)  # Fit on food labels

# Preprocess image
def preprocess_image(img_path, target_size=(224, 224)):
    img = tf.keras.utils.load_img(img_path, target_size=target_size)
    img = tf.keras.utils.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Predict food class and get calories from CSV
def predict_food(img_path):
    img = preprocess_image(img_path)
    preds = model.predict(img)  # Single output: class probabilities
    pred_class_index = np.argmax(preds, axis=1)[0]  # Get predicted class index
    food_name = label_encoder.inverse_transform([pred_class_index])[0]  # Decode label
    
    # Lookup calories from CSV
    calories_row = df[df['label'].str.lower() == food_name.lower()]
    if not calories_row.empty:
        calories = float(calories_row['calories'].values[0])
    else:
        calories = None  # Or some default value
    
    return food_name, round(calories, 2)

# Example usage
if __name__ == "__main__":
    test_image = "data\Porotta\porotta_2.jpeg"  # Replace with your test image path
    food, cal = predict_food(test_image)
    print(f"🍴 Predicted Food: {food}")
    print(f"🔥 Estimated Calories: {cal}")
