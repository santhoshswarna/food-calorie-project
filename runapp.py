import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# -----------------------
# Load model
# -----------------------
model = load_model("food_classifier_densenet201.h5")  # replace with your .h5 file

# Food labels (must match training classes order)
class_labels = ["Appam", "Biryani",  "Chapati","Dosa","Idli","Pongal", "Poori","Parotta", "Vada","White Rice"]

# Calories database
calorie_map = {
    "Appam": 117,
    "Biryani": 400,
    "Chapati": 120,
    "Dosa": 168,
    "Idli": 58,
    "Pongal": 250,
    "Poori": 101,   
    "Parotta": 240,
    "Vada": 155,  
    "White Rice": 206,
     
     
    
}

# -----------------------
# Prediction function
# -----------------------
def predict_food(image_path):
    image = Image.open(image_path).convert("RGB")
    img_resized = image.resize((224, 224))  # adjust if your model input differs
    img_array = img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    pred_index = np.argmax(preds[0])
    label = class_labels[pred_index]
    calories = calorie_map.get(label, "N/A")
    return label, calories, image

# -----------------------
# UI Functions
# -----------------------
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        label, calories, pil_image = predict_food(file_path)

        # Show image in UI
        img_display = pil_image.resize((250, 250))
        img_tk = ImageTk.PhotoImage(img_display)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # Show results
        result_label.config(text=f"Food: {label}\nCalories: {calories} kcal")

# -----------------------
# Tkinter Window
# -----------------------
root = tk.Tk()
root.title("Food Calorie Estimator")
root.geometry("400x450")

title = tk.Label(root, text="🍲 Food Calorie Estimator", font=("Arial", 16, "bold"))
title.pack(pady=10)

upload_btn = tk.Button(root, text="Upload Food Image", command=upload_image, font=("Arial", 12))
upload_btn.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

result_label = tk.Label(root, text="Upload an image to see result", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
