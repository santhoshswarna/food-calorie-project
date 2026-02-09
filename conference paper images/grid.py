import matplotlib.pyplot as plt
import os

image_folder = 'data/'
class_names = sorted(os.listdir(image_folder))[:10]  # get 10 classes
fig, axes = plt.subplots(2, 5, figsize=(10, 4))

for i, class_name in enumerate(class_names):
    img_list = os.listdir(os.path.join(image_folder, class_name))
    img_path = os.path.join(image_folder, class_name, img_list[0])  # First image in class
    img = plt.imread(img_path)
    ax = axes[i // 5, i % 5]
    ax.imshow(img)
    ax.set_title(class_name)
    ax.axis('off')

plt.tight_layout()
plt.savefig('samples_10_classes.png')
plt.show()
