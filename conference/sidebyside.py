import os
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# Load image
image_folder = 'data/'
class_name = sorted(os.listdir(image_folder))[4]  # Change index if needed
img_list = os.listdir(os.path.join(image_folder, class_name))
img_path = os.path.join(image_folder, class_name, img_list[0])

original_img = load_img(img_path, target_size=(224, 224))
orig_array = img_to_array(original_img) / 255.0
orig_array = np.expand_dims(orig_array, axis=0)

# Define a list of augmenters with descriptive names
augmenters = [
    ("Original", ImageDataGenerator()),
    ("Rotation 40°", ImageDataGenerator(rotation_range=40)),
    ("Width shift 20%", ImageDataGenerator(width_shift_range=0.2)),
    ("Height shift 20%", ImageDataGenerator(height_shift_range=0.2)),
    ("Shear 20%", ImageDataGenerator(shear_range=0.2)),
    ("Zoom 20%", ImageDataGenerator(zoom_range=0.2)),
    ("Horizontal Flip", ImageDataGenerator(horizontal_flip=True)),
    ("Vertical Flip", ImageDataGenerator(vertical_flip=True)),
]

# Plot augmented images in 2 rows and 4 columns
plt.figure(figsize=(10, 4))
for i, (name, datagen) in enumerate(augmenters):
    aug_iter = datagen.flow(orig_array, batch_size=1)
    aug_img = next(aug_iter)[0]
    plt.subplot(2, 4, i + 1)
    plt.imshow(aug_img)
    plt.title(name)
    plt.axis('off')

plt.tight_layout()
plt.savefig('all_augmentations_2x4.png')
plt.show()
