import os
from PIL import Image
import imagehash
from tqdm import tqdm

def compute_image_hashes(folder):
    hashes = {}
    for root, _, files in os.walk(folder):
        for file in tqdm(files, desc=f"Hashing {root}"):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(root, file)
                try:
                    img = Image.open(path)
                    h = imagehash.average_hash(img)
                    hashes[path] = str(h)
                except Exception as e:
                    print(f"Error with {path}: {e}")
    return hashes

# Paths to your datasets
train_duo = "./dataset/train/duolingo"
train_not = "./dataset/train/not_duolingo"
val_duo = "./dataset/validation/duolingo"
val_not = "./dataset/validation/not_duolingo"
test_duo = "./dataset/test/duolingo"
test_not = "./dataset/test/not_duolingo"

# Compute hashes
train_duo_hashes = compute_image_hashes(train_duo)
train_not_hashes = compute_image_hashes(train_not)
val_duo_hashes = compute_image_hashes(val_duo)
val_not_hashes = compute_image_hashes(val_not)
test_duo_hashes = compute_image_hashes(test_duo)
test_not_hashes = compute_image_hashes(test_not)

# Check overlaps
def find_overlaps(set1, set2, label1, label2):
    overlaps = set(set1.values()) & set(set2.values())
    if overlaps:
        print(f"Found {len(overlaps)} overlaps between {label1} and {label2}")
        for h in overlaps:
            paths1 = [p for p, v in set1.items() if v == h]
            paths2 = [p for p, v in set2.items() if v == h]
            print(f"Hash {h}: {paths1} <-> {paths2}")
    else:
        print(f"No overlaps between {label1} and {label2}")

find_overlaps(train_duo_hashes, val_duo_hashes, "Train Duolingo", "Val Duolingo")
find_overlaps(train_not_hashes, val_not_hashes, "Train Not Duolingo", "Val Not Duolingo")
find_overlaps(train_duo_hashes, test_duo_hashes, "Train Duolingo", "Test Duolingo")
find_overlaps(train_not_hashes, test_not_hashes, "Train Not Duolingo", "Test Not Duolingo")
find_overlaps(val_duo_hashes, test_duo_hashes, "Val Duolingo", "Test Duolingo")
find_overlaps(val_not_hashes, test_not_hashes, "Val Not Duolingo", "Test Not Duolingo")