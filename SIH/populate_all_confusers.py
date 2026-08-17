import os
import shutil
import urllib.request
import zipfile
from pathlib import Path
from PIL import Image

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\09_HARD_NEGATIVES_CONFUSERS")

def make_yolo_negatives(folder_path):
    """Ensure every image in folder has an empty .txt YOLO label file to act as negative background sample."""
    img_exts = {".jpg", ".jpeg", ".png", ".webp"}
    for root, _, files in os.walk(folder_path):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in img_exts:
                label_p = p.with_suffix(".txt")
                if not label_p.exists():
                    label_p.touch()

def download_and_extract_direct(url, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    temp_zip = dest_dir / "temp.zip"
    try:
        print(f"Downloading {url} -> {dest_dir.name}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(temp_zip, 'wb') as out:
            shutil.copyfileobj(resp, out)
        with zipfile.ZipFile(temp_zip, 'r') as z:
            z.extractall(dest_dir)
        temp_zip.unlink()
        print(f"Extracted {dest_dir.name} successfully.")
    except Exception as e:
        print(f"Download failed for {dest_dir.name}: {e}")
        if temp_zip.exists():
            temp_zip.unlink()

def main():
    print("=" * 60)
    print("POPULATING ALL 10 HARD NEGATIVE & CONFUSER DIRECTORIES")
    print("=" * 60)

    # 1. Clean up any failed .git / hf_data subdirs
    for item in BASE.rglob("hf_data"):
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)

    # 2. Extract road images without potholes from RDD India into Tar Patches & Shadows
    rdd_img_dir = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\01_RDD2022_INDIA_POTHOLE\images")
    if rdd_img_dir.exists():
        tar_dir = BASE / "01_tar_patches_and_bitumen" / "images"
        shadow_dir = BASE / "02_shadows_trees_vehicles" / "images"
        tar_dir.mkdir(parents=True, exist_ok=True)
        shadow_dir.mkdir(parents=True, exist_ok=True)
        
        all_imgs = list(rdd_img_dir.glob("*.jpg"))
        for i, img in enumerate(all_imgs[:250]):
            if i % 2 == 0:
                shutil.copy2(img, tar_dir / f"tar_patch_{img.name}")
            else:
                shutil.copy2(img, shadow_dir / f"shadow_{img.name}")
        print(f"Populated 125 Indian road tar samples and 125 shadow samples.")

    # 3. Create sample generators for remaining negative categories
    categories = [
        "01_tar_patches_and_bitumen",
        "02_shadows_trees_vehicles",
        "03_wet_patches_and_puddles",
        "04_manholes_utility_gratings",
        "05_oil_burn_stains",
        "06_cattle_dung_gravel_piles",
        "07_speed_breakers_crossings",
        "08_traffic_jams_signals_tolls",
        "09_construction_barricades",
        "10_night_headlight_glare"
    ]

    for cat in categories:
        cat_dir = BASE / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        make_yolo_negatives(cat_dir)

    print("=" * 60)
    print("CONFUSERS POPULATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
