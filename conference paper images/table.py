import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from sklearn.metrics import (
    classification_report, accuracy_score, confusion_matrix, top_k_accuracy_score
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.models import load_model

# ---- 1) Load trained model ----
model = load_model("food_classifier_densenet201.h5")  # adjust filename if different

# ---- 2) Test generator ----
test_dir = "split/test"   # folder containing class subfolders
img_size = (224, 224)
batch_size = 32

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_gen = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    shuffle=False,
    class_mode='categorical',
    batch_size=batch_size
)

# ---- 3) Ground truth and class names ----
y_true_indices = test_gen.classes
class_indices = test_gen.class_indices  # dict: {class_name: index}
class_names = [k for k, v in sorted(class_indices.items(), key=lambda kv: kv[1])]

# ---- 4) Predict probabilities for the whole test set ----
y_score = model.predict(test_gen, verbose=0)  # shape: [N, n_classes]

# ---- 5) Convert to predicted labels ----
y_pred_indices = np.argmax(y_score, axis=1)

# ---- 6) Overall accuracy ----
acc = accuracy_score(y_true_indices, y_pred_indices)

# ---- 7) Top-k accuracy ----
n_classes = y_score.shape[1]
k_top = min(5, n_classes)
topk = top_k_accuracy_score(y_true_indices, y_score, k=k_top)

# ---- 8) Per-class metrics ----
report_dict = classification_report(
    y_true_indices,
    y_pred_indices,
    target_names=class_names,
    output_dict=True,
    zero_division=0
)

# ---- 9) Confusion matrix ----
cm = confusion_matrix(y_true_indices, y_pred_indices)

# ---- 10) Save metrics to CSV ----
with open("per_class_metrics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Class", "Precision", "Recall", "F1-score", "Support"])
    for cname in class_names:
        row = report_dict[cname]
        w.writerow([
            cname,
            f"{row['precision']:.2f}",
            f"{row['recall']:.2f}",
            f"{row['f1-score']:.2f}",
            int(row['support'])
        ])

with open("overall_metrics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Metric", "Value"])
    w.writerow(["Overall Accuracy", f"{acc:.4f}"])
    w.writerow([f"Top-{k_top} Accuracy", f"{topk:.4f}"])

# ---- 11) Plot confusion matrix ----
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names,
            yticklabels=class_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

# ---- 12) Print results ----
print("✅ Evaluation Completed")
print("Overall Accuracy:", acc)
print(f"Top-{k_top} Accuracy:", topk)
print("Saved: per_class_metrics.csv, overall_metrics.csv, confusion_matrix.png")
