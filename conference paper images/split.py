import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Generate images.csv automatically
image_dir = "data"  # main folder with subfolders per label
data = []

for label in os.listdir(image_dir):
    label_dir = os.path.join(image_dir, label)
    if os.path.isdir(label_dir):
        for file in os.listdir(label_dir):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                data.append({
                    "filepath": os.path.join(label_dir, file),
                    "label": label
                })

df = pd.DataFrame(data)
df.to_csv("images.csv", index=False)
print("✅ images.csv created with", len(df), "entries")

# 2. Define split function
def copy_split(df_split, root):
    for _, r in df_split.iterrows():
        out_dir = os.path.join(root, r['label'])
        os.makedirs(out_dir, exist_ok=True)
        shutil.copy2(r['filepath'], out_dir)

# 3. Train/Val/Test split (70/15/15)
train_df, tmp_df = train_test_split(df, test_size=0.3, stratify=df['label'], random_state=42)
val_df, test_df = train_test_split(tmp_df, test_size=0.5, stratify=tmp_df['label'], random_state=42)

# 4. Copy images to folders
copy_split(train_df, "split/train")
copy_split(val_df,   "split/val")
copy_split(test_df,  "split/test")

print("✅ Data split completed!")
print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
