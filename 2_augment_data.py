"""
Data Augmentation for training dataset
Category B - Project 2: Pakistani Politician Image Classification
Apply to training set only: rotation, flipping, brightness, zoom, crop
"""

import os
import numpy as np
from pathlib import Path
from PIL import Image, ImageEnhance
import random

class DataAugmentation:
    """Apply various data augmentation techniques"""
    
    @staticmethod
    def rotate(image, angle_range=(-15, 15)):
        """Random rotation"""
        angle = random.uniform(angle_range[0], angle_range[1])
        return image.rotate(angle, expand=True, fillcolor='white')
    
    @staticmethod
    def flip(image, horizontal=True, vertical=False):
        """Flip image"""
        if random.random() > 0.5:
            if horizontal:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image
    
    @staticmethod
    def brightness_variation(image, factor_range=(0.7, 1.3)):
        """Adjust brightness"""
        factor = random.uniform(factor_range[0], factor_range[1])
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def zoom(image, zoom_range=(0.8, 1.0)):
        """Random zoom (crop from center)"""
        zoom_factor = random.uniform(zoom_range[0], zoom_range[1])
        width, height = image.size
        new_width = int(width * zoom_factor)
        new_height = int(height * zoom_factor)
        
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        
        cropped = image.crop((left, top, right, bottom))
        return cropped.resize((width, height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def random_crop(image, crop_percent=0.1):
        """Random crop"""
        width, height = image.size
        crop_width = int(width * (1 - crop_percent))
        crop_height = int(height * (1 - crop_percent))
        
        left = random.randint(0, width - crop_width)
        top = random.randint(0, height - crop_height)
        
        cropped = image.crop((left, top, left + crop_width, top + crop_height))
        return cropped.resize((width, height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def augment_image(image_path, augmentation_count=2):
        """Apply random augmentations to an image"""
        try:
            image = Image.open(image_path).convert('RGB')
            augmented_images = [image]  # Keep original
            
            for _ in range(augmentation_count):
                aug_image = image.copy()
                
                # Apply random augmentations
                if random.random() > 0.5:
                    aug_image = DataAugmentation.rotate(aug_image)
                if random.random() > 0.5:
                    aug_image = DataAugmentation.flip(aug_image, horizontal=True)
                if random.random() > 0.5:
                    aug_image = DataAugmentation.brightness_variation(aug_image)
                if random.random() > 0.5:
                    aug_image = DataAugmentation.zoom(aug_image)
                if random.random() > 0.5:
                    aug_image = DataAugmentation.random_crop(aug_image)
                
                augmented_images.append(aug_image)
            
            return augmented_images
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None

def augment_training_dataset(train_dir, augmentation_count=2):
    """
    Apply data augmentation to training dataset
    
    Args:
        train_dir: Path to training directory
        augmentation_count: Number of augmented versions per image
    """
    
    train_path = Path(train_dir)
    augmented_count = 0
    
    print("\n🔄 DATA AUGMENTATION (Training Set Only)")
    print("=" * 70)
    print(f"Augmentation: {augmentation_count} variants per image")
    print("Techniques: Rotation, Flip, Brightness, Zoom, Crop")
    print("=" * 70)
    
    # Get all class folders
    classes = sorted([d for d in train_path.iterdir() if d.is_dir()])
    
    for class_folder in classes:
        class_name = class_folder.name
        print(f"\nAugmenting: {class_name}")
        
        # Get all images
        images = [f for f in class_folder.iterdir() 
                 if f.suffix.lower() in ['.jpg', '.jpeg', '.jfif', '.png']]
        
        original_count = len(images)
        
        for idx, img_path in enumerate(images, 1):
            augmented = DataAugmentation.augment_image(img_path, augmentation_count)
            
            if augmented:
                # Save augmented versions
                stem = img_path.stem
                for aug_idx, aug_image in enumerate(augmented[1:], 1):  # Skip original
                    new_filename = f"{stem}_aug_{aug_idx}{img_path.suffix}"
                    new_path = class_folder / new_filename
                    aug_image.save(new_path, quality=95)
                    augmented_count += 1
            
            if idx % 10 == 0:
                print(f"  Processed {idx}/{original_count} images...")
        
        new_count = len([f for f in class_folder.iterdir() if f.is_file()])
        added = new_count - original_count
        print(f"  ✓ {class_name}: {original_count} → {new_count} images (+{added})")
    
    print("\n" + "=" * 70)
    print(f"✓ Augmentation complete!")
    print(f"  Total augmented images created: {augmented_count}")
    print("=" * 70)

if __name__ == "__main__":
    # Configuration
    TRAIN_DIR = "dataset_split/train"
    AUGMENTATION_COUNT = 2  # 2 additional versions per image
    
    if not Path(TRAIN_DIR).exists():
        print(f"❌ Training directory not found: {TRAIN_DIR}")
        print("   Run '1_split_dataset.py' first")
    else:
        augment_training_dataset(TRAIN_DIR, AUGMENTATION_COUNT)
