from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255)

generator = datagen.flow_from_directory(
    "data",              # 👈 SAME folder used in training
    target_size=(224, 224),
    batch_size=1,
    class_mode="categorical"
)

print("\n✅ MODEL CLASS ORDER (VERY IMPORTANT):")
for label, index in generator.class_indices.items():
    print(f"{index} → {label}")
