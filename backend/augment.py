import os
import cv2
import ssl
from albumentations import (
    Compose, HorizontalFlip, RandomRotate90,
    RandomBrightnessContrast, HueSaturationValue,
    ShiftScaleRotate, OneOf, GaussianBlur, MotionBlur,
    ISONoise
)
from tqdm import tqdm
import argparse
from multiprocessing import Pool, cpu_count

# Fix SSL certificate issue on Mac
ssl._create_default_https_context = ssl._create_unverified_context

class ImageAugmentor:
    def __init__(self, input_folder, output_folder, augmentations_per_image=3):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.augmentations_per_image = augmentations_per_image
        
        # Supported image extensions
        self.image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
        
        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Define our augmentation pipeline
        self.augmentation_pipeline = Compose([
            # Geometric transformations
            HorizontalFlip(p=0.5),
            RandomRotate90(p=0.3),
            ShiftScaleRotate(
                shift_limit=0.05, 
                scale_limit=0.1, 
                rotate_limit=30, 
                p=0.5
            ),
            
            # Color transformations
            RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=20, p=0.5),
            
            # Mild blur/noise for robustness
            OneOf([
                GaussianBlur(blur_limit=3, p=0.5),
                MotionBlur(blur_limit=3, p=0.5),
            ], p=0.3),
            
            # Optional: mild noise
            ISONoise(p=0.2),
        ], p=1.0)
    
    def augment_image(self, image_path):
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            
            # Save original image to output folder (optional)
            # output_path = os.path.join(self.output_folder, f"{base_name}_original.jpg")
            # cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            
            # Generate augmented versions
            for i in range(self.augmentations_per_image):
                augmented = self.augmentation_pipeline(image=image)
                augmented_image = augmented["image"]
                
                # Convert back to BGR for saving
                augmented_image_bgr = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)
                
                # Save augmented image
                output_path = os.path.join(
                    self.output_folder, 
                    f"{base_name}_aug_{i+1}.jpg"
                )
                cv2.imwrite(output_path, augmented_image_bgr)
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    def process_folder(self):
        # Get all image files in input folder
        image_files = []
        for root, _, files in os.walk(self.input_folder):
            for file in files:
                if file.lower().endswith(self.image_extensions):
                    image_files.append(os.path.join(root, file))
        
        print(f"Found {len(image_files)} images to augment.")
        print(f"Generating {self.augmentations_per_image} augmentations per image...")
        
        # Use multiprocessing to speed up augmentation
        with Pool(processes=max(1, cpu_count() - 1)) as pool:
            list(tqdm(
                pool.imap(self.augment_image, image_files),
                total=len(image_files),
                desc="Augmenting images"
            ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image Augmentation for Machine Learning')
    parser.add_argument('input_folder', help='Path to folder containing original images')
    parser.add_argument('output_folder', help='Path to save augmented images')
    parser.add_argument('--augmentations', type=int, default=5,
                       help='Number of augmentations to generate per image (default: 5)')
    
    args = parser.parse_args()
    
    # Verify input folder exists
    if not os.path.isdir(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist.")
        exit(1)
    
    # Create augmentor and process
    augmentor = ImageAugmentor(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        augmentations_per_image=args.augmentations
    )
    augmentor.process_folder()
    
    print("\nImage augmentation completed successfully!")
