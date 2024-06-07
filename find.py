from genericpath import isdir
import imagehash
from PIL import Image
from os import walk, unlink
import argparse

def get_image_files(folder):
    image_files = []
    for root, _, files in walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append((root, file))
    return image_files

parser = argparse.ArgumentParser(description="Test")
parser.add_argument("--delete", action='store_true',
                    default=False, help="Deletes duplicates")
parser.add_argument("--folder", default="dataset", help="Dataset folder name")

args = parser.parse_args()

folder_name = args.folder

if not isdir(folder_name):
    print("Please provide a valid folder name or create a folder named dataset")
    exit()

image_files = get_image_files(folder_name)
hash_history = {}
duplicate_hashes = []

for i, (root, image_name) in enumerate(image_files):
    try:
        # Hash the image
        image_path = f"{root}/{image_name}"
        hashed = imagehash.average_hash(Image.open(image_path))

        if hashed in hash_history:
            hash_history[hashed].append(image_path)
            # Mark hash as duplicate
            if hashed not in duplicate_hashes:
                duplicate_hashes.append(hashed)
        else:
            hash_history[hashed] = [image_path]

        # Clearing console output
        print("\033[H\033[J", end="")
    except Exception as e:
        print(f"Error with image {image_name} in {root}: {str(e)}")

    print(f"Progress: {i+1}/{len(image_files)}")

# Clearing console output
print("\033[H\033[J", end="")

deleted = 0
for hash in duplicate_hashes:
    # Print duplicates
    joined = ", ".join(hash_history[hash])
    print(f"\033[0;91mDuplicate images: \033[0m{joined}")

    # Delete duplicates if --delete is set to True
    if args.delete:
        for i, image in enumerate(hash_history[hash]):
            # Skip first image
            if i == 0:
                continue

            # Delete image
            unlink(image)
            deleted += 1

if len(duplicate_hashes):
    print(f"Found {len(duplicate_hashes)} duplicates")

    if args.delete:
        print(f"\033[0;91mDeleted {deleted} images from dataset")
else:
    print(f"No duplicates found!")

# Reset console color
print("\033[0m")