from modules.predictor import FoodPredictor

def main():
    predictor = FoodPredictor()
    
    img_path = "dataset/test/Apple/apple_1.jpg"  # Example
    food, qty, cal = predictor.predict(img_path)

    if cal:
        print(f"Detected: {food}")
        print(f"Quantity: {qty}")
        print(f"Calories: {cal} kcal")
    else:
        print("Food not found in calorie database.")

if __name__ == "__main__":
    main()
# python modules/predictor.py data/test/apple/1.jpg
