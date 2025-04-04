import os
import glob
from tqdm import tqdm

def delete_augmented_files(directory, dry_run=False):
    """
    Delete all files containing '_aug_' in their names.
    
    Args:
        directory (str): Path to directory to search
        dry_run (bool): If True, only show what would be deleted without actually deleting
    """
    # Find all files with '_aug_' in the name (case insensitive)
    pattern = os.path.join(directory, '**', '*_aug_*')
    augmented_files = glob.glob(pattern, recursive=True)
    
    if not augmented_files:
        print(f"No files containing '_aug_' found in {directory}")
        return
    
    print(f"Found {len(augmented_files)} files containing '_aug_'")
    
    if dry_run:
        print("\nDry run mode - no files will be deleted")
    
    deleted_count = 0
    errors = []
    
    for file_path in tqdm(augmented_files, desc="Processing files"):
        try:
            if dry_run:
                print(f"[Dry Run] Would delete: {file_path}")
            else:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_count += 1
                else:
                    errors.append(f"Not a file: {file_path}")
        except Exception as e:
            errors.append(f"Error deleting {file_path}: {str(e)}")
    
    if not dry_run:
        print(f"\nSuccessfully deleted {deleted_count}/{len(augmented_files)} files")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f" - {error}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Delete files containing "_aug_" in their names')
    parser.add_argument('directory', help='Directory to search for files')
    parser.add_argument('--dry-run', action='store_true',
                      help='Show what would be deleted without actually deleting')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        exit(1)
    
    delete_augmented_files(args.directory, args.dry_run)