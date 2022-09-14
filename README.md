# Dataset Duplicate Finder
It is a script for detecting and deleting duplicate images in a dataset.

<hr>
## Usage
Create a folder named dataset (if doesn't exists). Then, put your images in that folder. The script will automatically detect duplicate images in your dataset.

## How it works?
The script uses **imagehash** library to calculate the hash of each image. Then, it compares the hashes of each image with the other images. If the image hashes are equal, the images are considered as duplicates.

## Installation
```
pip install -r requirements.txt
```

## Flags
* **--delete** : Automatically delete duplicate images.
* **--folder** : Specify the dataset folder name. Default is **dataset**.