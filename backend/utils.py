import os
from PIL import Image

# Resize all images to 224x224 (for MobileNetV2)
TARGET_SIZE = (224, 224)

def preprocess_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for img_name in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_name)
        try:
            img = Image.open(img_path).convert("RGB")
            img = img.resize(TARGET_SIZE)
            img.save(os.path.join(output_dir, img_name))
        except Exception as e:
            print(f"Skipping {img_name}: {e}")