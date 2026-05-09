# Image Person Filter and Crop Script

## How to Use

### Option 1: One-Click Method (Easiest)
1. **Double-click** `Renumber_Images.bat`
2. A folder selection dialog will appear
3. Select the folder containing your images
4. The script will:
	- keep images with one detected person
	- delete images with no detected person
	- crop images with multiple people to the main person

### Option 2: Command Line Method
```
python rename_images.py "path\to\folder"
```

## Supported Image Formats
- .jpg / .jpeg
- .jfif
- .png
- .bmp
- .gif
- .tiff
- .webp

## Features
✓ Detects faces first, then falls back to full-body person detection
✓ Keeps single-person images unchanged
✓ Deletes images with no person detected
✓ Crops multi-person images to the main person
✓ Works recursively through subfolders by default
✓ One-click operation
✓ Shows detailed processing log

## Notes
- The script edits files in place by default
- Multi-person images are cropped to the largest/most central detected person
- Images with no detection are deleted unless you use `--no-delete`
- Use `--copy-crops` if you want cropped images saved as new files instead of overwriting originals

## Requirements
- Python 3.x installed
- tkinter library (usually included with Python)
- opencv-python

Install OpenCV if needed:
```bash
pip install opencv-python
```

## Example
If an image has one person, it stays as it is.
If an image has two people, the script crops the main person and overwrites the file.
If no person is detected, the image is deleted.
