from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from predict import predict_bytes
import pandas as pd

app = FastAPI()

# Load CSV
food_df = pd.read_csv("food_labels.csv")

@app.get("/")
def home():
    return {"message": "Food Classification API is running 🚀"}

@app.post("/predict")
async def predict_food(file: UploadFile = File(...)):
    image_bytes = await file.read()

    class_index, confidence = predict_bytes(image_bytes)

    food_name = food_df.iloc[class_index]["label"]
    calories = float(food_df.iloc[class_index]["calories"])

    return JSONResponse({
        "food": food_name,
        "calories": calories,
        "confidence": round(confidence * 100, 2)
    })
