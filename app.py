from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_bytes
import pandas as pd

app = FastAPI(title="Food Calorie Estimator API")

# ✅ Enable CORS for Flutter / Mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (safe for demo/project)
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load CSV safely
try:
    food_df = pd.read_csv("food_labels.csv")
except Exception as e:
    print("Error loading CSV:", e)
    food_df = None


@app.get("/")
def home():
    return {"message": "Food Classification API is running 🚀"}


@app.post("/predict")
async def predict_food(file: UploadFile = File(...)):
    if food_df is None:
        raise HTTPException(status_code=500, detail="Food labels CSV not loaded")

    try:
        image_bytes = await file.read()

        class_index, confidence = predict_bytes(image_bytes)

        # Safety check
        if class_index >= len(food_df):
            raise HTTPException(status_code=400, detail="Invalid prediction index")

        food_name = food_df.iloc[class_index]["label"]
        calories = float(food_df.iloc[class_index]["calories"])

        return JSONResponse({
            "food": food_name,
            "calories": calories,
            "confidence": round(confidence * 100, 2)
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
