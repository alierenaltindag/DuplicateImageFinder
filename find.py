from genericpath import isdir
import imagehash
from PIL import Image
from os import listdir, unlink
import argparse

parser = argparse.ArgumentParser(description="Test")
parser.add_argument("--delete", action='store_true',
                    default=False, help="Deletes duplicates")
parser.add_argument("--folder", default="dataset", help="Dataset folder name")

args = parser.parse_args()

folder_name = args.folder

if not isdir(folder_name):
    print("Please provide a valid folder name or create a folder named dataset")
    exit()

dataset = listdir(folder_name)
hash_history = {}
duplicate_hashes = []
for i, image_name in enumerate(dataset):
    if (not image_name.endswith(".png")) & (not image_name.endswith(".jpg")) & (not image_name.endswith(".jpeg")):
        continue

    try:
        # Hash the image
        hashed = imagehash.average_hash(
            Image.open(f"./{folder_name}/{image_name}"))

        if(hashed in hash_history):
            hash_history[hashed].append(image_name)
            # Mark hash as duplicate
            if(not hashed in duplicate_hashes):
                duplicate_hashes.append(hashed)
        else:
            hash_history[hashed] = [image_name]

        # Clearing console output
        print("\033[H\033[J", end="")
    except:
        print("Error with image: " + image_name)

    print(f"Progress: {i+1}/{len(dataset)}")

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
            if(i == 0):
                continue

            # Delete image
            unlink(f"dataset/{image}")
            deleted += 1

if(len(duplicate_hashes)):
    print(f"Found {len(duplicate_hashes)} duplicates")

    if args.delete:
        print(f"\033[0;91mDeleted {deleted} images from dataset")
else:
    print(f"No duplicates found!")

# # Reset console color
print("\033[0m")
