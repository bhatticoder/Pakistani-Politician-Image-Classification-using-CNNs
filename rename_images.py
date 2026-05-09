import os
import sys
from pathlib import Path
from tkinter import Tk, filedialog
import shutil

def renumber_images(folder_path):
    """Renumber all images in a folder sequentially."""
    
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        return False
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.jfif', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    # Get all image files
    image_files = []
    for file in os.listdir(folder_path):
        if os.path.splitext(file)[1].lower() in image_extensions:
            image_files.append(file)
    
    if not image_files:
        print(f"No image files found in {folder_path}")
        return False
    
    # Sort files (natural sort if possible)
    image_files.sort(key=lambda x: (
        int(''.join(filter(str.isdigit, x)) or '0'),
        x
    ))
    
    print(f"\nFound {len(image_files)} images in: {folder_path}")
    print("Renumbering images...\n")
    
    # Rename files sequentially
    rename_count = 0
    for index, filename in enumerate(image_files, 1):
        old_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1]
        new_filename = f"{index}{ext}"
        new_path = os.path.join(folder_path, new_filename)
        
        if old_path != new_path:
            try:
                shutil.move(old_path, new_path)
                print(f"  {filename} → {new_filename}")
                rename_count += 1
            except Exception as e:
                print(f"  Error renaming {filename}: {e}")
        else:
            print(f"  {filename} (no change needed)")
    
    print(f"\n✓ Successfully renumbered {rename_count} images!")
    return True

def main():
    # If folder path provided as argument, use it
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # Open folder selection dialog
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        folder_path = filedialog.askdirectory(title="Select folder with images to renumber")
        root.destroy()
        
        if not folder_path:
            print("No folder selected. Exiting.")
            return
    
    renumber_images(folder_path)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
