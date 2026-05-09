import os
import subprocess
from pathlib import Path

# Configuration
DATASET_SLUG = "YOUR_USERNAME/YOUR_DATASET_NAME"  # Change this!
DATASET_DIR = r"g:\Fast\Semester 6\DataSet for Project 2"

# Get list of folders to upload
folders = [f for f in os.listdir(DATASET_DIR) 
           if os.path.isdir(os.path.join(DATASET_DIR, f))]

print(f"Found {len(folders)} folders to upload:")
for folder in folders:
    print(f"  - {folder}")

# Step 1: Upload dataset metadata
print("\n[1/3] Creating dataset metadata...")
metadata = {
    "id": DATASET_SLUG,
    "licenses": [{"name": "CC0-1.0"}],
    "resources": []
}

import json
os.makedirs(f"{DATASET_DIR}\\dataset_upload", exist_ok=True)
with open(f"{DATASET_DIR}\\dataset_upload\\dataset-metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Metadata created at: dataset_upload\\dataset-metadata.json")

# Step 2: Upload to Kaggle
print("\n[2/3] Uploading to Kaggle...")
print(f"Dataset slug: {DATASET_SLUG}")
print("\nRun this command to upload:")
print(f"kaggle datasets create-version --p-dir {DATASET_DIR} --message 'Initial upload'")

print("\n[3/3] Next steps:")
print("1. If this is your first upload, run:")
print(f"   kaggle datasets create --p-dir {DATASET_DIR}")
print("\n2. For subsequent uploads, run:")
print(f"   kaggle datasets version --p-dir {DATASET_DIR} --message 'Updated dataset'")
