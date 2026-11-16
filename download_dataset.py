"""
Dataset Acquisition & Setup Utility for PlantVillage Dataset
Downloads and structures the PlantVillage dataset into ./data/PlantVillage
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

DATA_DIR = Path("./data/PlantVillage")


def download_with_kagglehub():
    """Download using modern kagglehub API."""
    try:
        import kagglehub
        print("[*] Downloading latest PlantVillage dataset via kagglehub...")
        path = kagglehub.dataset_download("emmarex/plantdisease")
        print(f"[✓] Download completed to cache: {path}")

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        # Check source folder
        source = Path(path)
        print(f"[*] Copying/linking dataset to {DATA_DIR}...")

        # If it has PlantVillage or subfolder
        subfolders = [p for p in source.glob("**/*") if p.is_dir() and "PlantVillage" in p.name]
        target_src = subfolders[0] if subfolders else source

        for item in target_src.iterdir():
            dest = DATA_DIR / item.name
            if not dest.exists():
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)

        print(f"[✓] Dataset successfully staged in: {DATA_DIR.resolve()}")
        return True
    except ImportError:
        print("[!] 'kagglehub' is not installed. Run: pip install kagglehub")
        return False
    except Exception as e:
        print(f"[!] kagglehub download encountered an error: {e}")
        return False


def print_manual_instructions():
    print("""
======================================================================
MANUAL DATASET DOWNLOAD INSTRUCTIONS
======================================================================
1. Download PlantVillage from Kaggle:
   URL: https://www.kaggle.com/datasets/emmarex/plantdisease
   or:  https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

2. Using Kaggle CLI:
   kaggle datasets download -d emmarex/plantdisease
   tar -xf plantdisease.zip -C ./data/PlantVillage

3. Ensure directory structure matches:
   data/
   └── PlantVillage/
       ├── Apple___Apple_scab/
       ├── Apple___Black_rot/
       ├── Apple___Cedar_apple_rust/
       ├── Apple___healthy/
       ├── Blueberry___healthy/
       ├── ...
       └── Tomato___healthy/
======================================================================
""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download PlantVillage Dataset")
    parser.add_argument("--manual", action="store_true", help="Print manual download instructions")
    args = parser.parse_args()

    if args.manual:
        print_manual_instructions()
    else:
        success = download_with_kagglehub()
        if not success:
            print_manual_instructions()

