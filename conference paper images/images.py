import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Parameters
IMAGE_FOLDER = 'data/'  # Replace with your dataset folder path
SAVE_FOLDER = 'augmented_grid_samples/'
IMG_SIZE = (224, 224)
BATCH_SIZE = 10  # Number of images to show in the grid

# Create directory to save images if not exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Data generator with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

# Flow images from directory
train_generator = train_datagen.flow_from_directory(
    IMAGE_FOLDER,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Get one batch of images
images, labels = next(train_generator)

# Plot images as grid
fig, axes = plt.subplots(2, 5, figsize=(8, 6))
axes = axes.flatten()

for img, ax in zip(images, axes):
    ax.imshow(img)
    ax.axis('off')

plt.tight_layout()
plt.suptitle('Augmented Images Grid', fontsize=16)
plt.subplots_adjust(top=0.88)

# Save the grid image
save_path = os.path.join(SAVE_FOLDER, 'augmented_images_grid.png')
plt.savefig(save_path)
plt.show()

print(f"Augmented images grid saved at: {save_path}")
