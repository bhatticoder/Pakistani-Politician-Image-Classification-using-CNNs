#!/usr/bin/env python3
"""
Kaggle Dataset Upload Script for Pakistani Politicians Dataset
Uploads to Kaggle for CNN image classification project
"""

import os
import json
import argparse
import subprocess
from pathlib import Path

def create_dataset_metadata(dataset_slug):
    """Create dataset-metadata.json for Kaggle"""
    metadata = {
        "id": dataset_slug,
        "licenses": [
            {
                "name": "CC0-1.0"
            }
        ],
        "resources": []
    }
    return metadata

def check_kaggle_credentials():
    """Check if Kaggle credentials exist"""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("❌ ERROR: Kaggle credentials not found!")
        print(f"   Expected location: {kaggle_json}")
        print("\n📋 STEPS TO FIX:")
        print("1. Go to: https://www.kaggle.com/account")
        print("2. Click 'Create New Token'")
        print("3. Download kaggle.json")
        print(f"4. Create folder: {kaggle_dir}")
        print(f"5. Move kaggle.json to: {kaggle_json}")
        print("6. Run this script again")
        return False
    
    print("✓ Kaggle credentials found!")
    return True

def upload_dataset(dataset_slug, dataset_dir, is_create=True, message=""):
    """Upload dataset to Kaggle"""
    
    if not check_kaggle_credentials():
        return False
    
    dataset_dir = Path(dataset_dir)
    if not dataset_dir.exists():
        print(f"❌ Dataset directory not found: {dataset_dir}")
        return False
    
    # Create metadata file in dataset directory
    metadata_path = dataset_dir / "dataset-metadata.json"
    metadata = create_dataset_metadata(dataset_slug)
    
    print(f"\n📝 Creating metadata file: {metadata_path}")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print("✓ Metadata created")
    
    # Prepare upload command
    os.chdir(dataset_dir)
    
    if is_create:
        print(f"\n🚀 Creating new dataset on Kaggle: {dataset_slug}")
        cmd = [
            "python", "-m", "kaggle", "datasets", "create",
            "--dir-mode", "tar",
            "-p", str(dataset_dir)
        ]
    else:
        print(f"\n🔄 Updating dataset on Kaggle: {dataset_slug}")
        if not message:
            message = "Updated dataset version"
        cmd = [
            "python", "-m", "kaggle", "datasets", "version",
            "--dir-mode", "tar",
            "-p", str(dataset_dir),
            "-m", message
        ]
    
    try:
        print(f"\n⏳ Starting upload... This may take 5-30 minutes depending on file size")
        print("-" * 50)
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print("-" * 50)
            print("✓ Upload successful!")
            print(f"\n🎉 Dataset available at: https://www.kaggle.com/datasets/{dataset_slug}")
            return True
        else:
            print("-" * 50)
            print("❌ Upload failed. Check the error messages above.")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Upload Pakistani Politicians dataset to Kaggle",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First time create
  python upload_dataset.py --create --slug "yourusername/pakistani-politicians-face-dataset"
  
  # Update existing dataset
  python upload_dataset.py --update --slug "yourusername/pakistani-politicians-face-dataset" --message "Added more images"
        """
    )
    
    parser.add_argument("--create", action="store_true", help="Create new dataset on Kaggle")
    parser.add_argument("--update", action="store_true", help="Update existing dataset version")
    parser.add_argument("--slug", required=True, help="Dataset slug (format: username/dataset-name)")
    parser.add_argument("--message", default="", help="Version message (for updates)")
    parser.add_argument("--dir", default=".", help="Dataset directory (default: current directory)")
    
    args = parser.parse_args()
    
    if not args.create and not args.update:
        parser.print_help()
        print("\n❌ Must use either --create or --update")
        return False
    
    if args.create and args.update:
        print("❌ Use either --create or --update, not both")
        return False
    
    print("=" * 60)
    print("🎯 KAGGLE DATASET UPLOAD")
    print("=" * 60)
    print(f"Dataset Slug: {args.slug}")
    print(f"Dataset Dir:  {args.dir}")
    print(f"Operation:    {'CREATE' if args.create else 'UPDATE'}")
    print("=" * 60)
    
    success = upload_dataset(
        dataset_slug=args.slug,
        dataset_dir=args.dir,
        is_create=args.create,
        message=args.message
    )
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
