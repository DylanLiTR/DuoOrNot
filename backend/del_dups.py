import os
import hashlib
from PIL import Image
import imagehash
from collections import defaultdict
import shutil

def find_duplicates(folder_path, hash_size=8, max_distance=5, move_to_folder=None):
    """
    Find and handle duplicate images in a folder.
    
    Parameters:
    - folder_path: Path to the folder containing images
    - hash_size: Size of the hash (8 is good for most cases)
    - max_distance: Maximum hash distance to consider images as duplicates
    - move_to_folder: If specified, moves duplicates here instead of deleting
    """
    # Create dictionary to store hashes
    hashes = defaultdict(list)
    
    # Supported image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    # Create folder for duplicates if needed
    if move_to_folder and not os.path.exists(move_to_folder):
        os.makedirs(move_to_folder)
    
    print(f"Scanning {folder_path} for duplicate images...")
    
    # Walk through all files in the folder
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(image_extensions):
                filepath = os.path.join(root, filename)
                
                try:
                    # Calculate perceptual hash of the image
                    with Image.open(filepath) as img:
                        # Convert to RGB if needed
                        if img.mode not in ('RGB', 'L'):
                            img = img.convert('RGB')
                        img_hash = str(imagehash.phash(img, hash_size=hash_size))
                        
                    # Add to our dictionary
                    hashes[img_hash].append(filepath)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
    
    print(f"\nFound {len(hashes)} unique images.")
    
    # Find duplicates by comparing hashes
    duplicate_groups = []
    hash_list = list(hashes.keys())
    
    for i, hash1 in enumerate(hash_list):
        for hash2 in hash_list[i+1:]:
            # Calculate hamming distance between hashes
            distance = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
            if distance <= max_distance:
                # Combine the groups
                combined = hashes[hash1] + hashes[hash2]
                duplicate_groups.append(combined)
                # Remove the hashes to avoid duplicate groups
                if hash1 in hashes:
                    del hashes[hash1]
                if hash2 in hashes:
                    del hashes[hash2]
                break
    
    # Add remaining groups with multiple files
    for hash_val, files in hashes.items():
        if len(files) > 1:
            duplicate_groups.append(files)
    
    total_duplicates = sum(len(group) - 1 for group in duplicate_groups)
    print(f"Found {total_duplicates} duplicate images in {len(duplicate_groups)} groups.")
    
    # Process duplicate groups
    for i, group in enumerate(duplicate_groups, 1):
        print(f"\nDuplicate group {i}:")
        
        # Keep the first file as original
        original = group[0]
        duplicates = group[1:]
        
        print(f"Original: {original}")
        
        for dup in duplicates:
            print(f"Duplicate: {dup}")
            
            if move_to_folder:
                # Move duplicate to another folder
                try:
                    dest = os.path.join(move_to_folder, os.path.basename(dup))
                    # Handle naming conflicts
                    counter = 1
                    while os.path.exists(dest):
                        name, ext = os.path.splitext(os.path.basename(dup))
                        dest = os.path.join(move_to_folder, f"{name}_{counter}{ext}")
                        counter += 1
                    shutil.move(dup, dest)
                    print(f"Moved to: {dest}")
                except Exception as e:
                    print(f"Error moving file: {e}")
            else:
                # Delete the duplicate
                try:
                    os.remove(dup)
                    print("Deleted successfully")
                except Exception as e:
                    print(f"Error deleting file: {e}")
    
    print("\nDuplicate removal process completed.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Find and remove duplicate images in a folder.')
    parser.add_argument('folder', help='Path to the folder containing images')
    parser.add_argument('--move-to', help='Move duplicates to this folder instead of deleting')
    parser.add_argument('--hash-size', type=int, default=8, 
                       help='Perceptual hash size (default: 8)')
    parser.add_argument('--max-distance', type=int, default=5,
                       help='Maximum hash distance to consider images as duplicates (default: 5)')
    
    args = parser.parse_args()
    
    # Verify folder exists
    if not os.path.isdir(args.folder):
        print(f"Error: Folder '{args.folder}' does not exist.")
        exit(1)
    
    # Verify move-to folder if specified
    if args.move_to and not os.path.exists(args.move_to):
        os.makedirs(args.move_to)
    
    find_duplicates(
        folder_path=args.folder,
        hash_size=args.hash_size,
        max_distance=args.max_distance,
        move_to_folder=args.move_to
    )