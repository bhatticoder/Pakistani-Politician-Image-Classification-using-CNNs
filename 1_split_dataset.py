"""
Split dataset into train (75%), validation (15%), and test (10%)
Category B - Project 2: Pakistani Politician Image Classification
"""

import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

def create_split_structure(source_dir, output_dir, train_ratio=0.75, val_ratio=0.15, test_ratio=0.10):
    """
    Split dataset into train/val/test directories
    
    Args:
        source_dir: Directory containing class folders
        output_dir: Output directory for train/val/test split
        train_ratio: Training set ratio (default 0.75)
        val_ratio: Validation set ratio (default 0.15)
        test_ratio: Test set ratio (default 0.10)
    """
    
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # Create output structure
    train_dir = output_path / "train"
    val_dir = output_path / "val"
    test_dir = output_path / "test"
    
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all class folders (skip hidden folders and .venv)
    classes = [d for d in source_path.iterdir() 
               if d.is_dir() and not d.name.startswith('.') and d.name != '.venv']
    
    print(f"Found {len(classes)} classes")
    print("=" * 70)
    
    stats = defaultdict(lambda: {"train": 0, "val": 0, "test": 0, "total": 0})
    
    for class_folder in sorted(classes):
        class_name = class_folder.name
        print(f"\nProcessing: {class_name}")
        
        # Get all images
        images = [f for f in class_folder.iterdir() 
                 if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.jfif', '.png', '.bmp']]
        
        if not images:
            print(f"  ⚠️  No images found in {class_name}")
            continue
        
        # Shuffle and split
        random.shuffle(images)
        total = len(images)
        
        train_count = int(total * train_ratio)
        val_count = int(total * val_ratio)
        
        train_images = images[:train_count]
        val_images = images[train_count:train_count + val_count]
        test_images = images[train_count + val_count:]
        
        # Create class folders in each split
        train_class_dir = train_dir / class_name
        val_class_dir = val_dir / class_name
        test_class_dir = test_dir / class_name
        
        train_class_dir.mkdir(exist_ok=True)
        val_class_dir.mkdir(exist_ok=True)
        test_class_dir.mkdir(exist_ok=True)
        
        # Copy files
        for img in train_images:
            shutil.copy2(img, train_class_dir / img.name)
        
        for img in val_images:
            shutil.copy2(img, val_class_dir / img.name)
        
        for img in test_images:
            shutil.copy2(img, test_class_dir / img.name)
        
        # Statistics
        stats[class_name]["train"] = len(train_images)
        stats[class_name]["val"] = len(val_images)
        stats[class_name]["test"] = len(test_images)
        stats[class_name]["total"] = total
        
        print(f"  Train: {len(train_images):3d} | Val: {len(val_images):2d} | Test: {len(test_images):2d} | Total: {total:3d}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("DATASET SPLIT SUMMARY")
    print("=" * 70)
    
    total_train = sum(s["train"] for s in stats.values())
    total_val = sum(s["val"] for s in stats.values())
    total_test = sum(s["test"] for s in stats.values())
    total_all = total_train + total_val + total_test
    
    print(f"\n{'Class':<30} {'Train':>6} {'Val':>5} {'Test':>5} {'Total':>6}")
    print("-" * 70)
    for class_name in sorted(stats.keys()):
        s = stats[class_name]
        print(f"{class_name:<30} {s['train']:>6} {s['val']:>5} {s['test']:>5} {s['total']:>6}")
    
    print("-" * 70)
    print(f"{'TOTAL':<30} {total_train:>6} {total_val:>5} {total_test:>5} {total_all:>6}")
    print(f"\nPercentages:")
    print(f"  Train: {total_train/total_all*100:.1f}% ({total_train} images)")
    print(f"  Val:   {total_val/total_all*100:.1f}% ({total_val} images)")
    print(f"  Test:  {total_test/total_all*100:.1f}% ({total_test} images)")
    print("=" * 70)
    
    print(f"\n✓ Dataset split complete!")
    print(f"  Train: {train_dir}")
    print(f"  Val:   {val_dir}")
    print(f"  Test:  {test_dir}")

if __name__ == "__main__":
    # Configuration
    SOURCE_DIR = "."  # Current directory with class folders
    OUTPUT_DIR = "dataset_split"  # Output directory
    
    print("\n🔀 DATASET SPLITTING (75% Train / 15% Val / 10% Test)")
    print("=" * 70)
    
    create_split_structure(SOURCE_DIR, OUTPUT_DIR)
