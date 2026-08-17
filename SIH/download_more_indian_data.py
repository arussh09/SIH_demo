import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

def download_and_extract_github(repo_url, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        print(f"Cloning {repo_url} -> {dest_dir.name}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, str(dest_dir)], check=True)
        print(f"Successfully cloned into {dest_dir.name}")
    except Exception as e:
        print(f"Error cloning {repo_url}: {e}")

def main():
    print("=" * 60)
    print("DOWNLOADING ADDITIONAL HIGH-QUALITY INDIAN ROAD DATASETS")
    print("=" * 60)

    # 1. Indian Speed Breakers & Road Hazards
    dest_speed = BASE / "10_INDIAN_SPEED_BREAKERS_AND_HAZARDS"
    download_and_extract_github("https://github.com/saisantosh1012/speed-breaker-pothole-detection-system-using-python.git", dest_speed)

    # 2. Road Distress & Indian Pavement Damage Repository
    dest_distress = BASE / "11_INDIAN_ROAD_DISTRESS_BENCHMARK"
    download_and_extract_github("https://github.com/sivakanth1/Detecting_Road_Damage.git", dest_distress)

    # 3. Create YOLO Negative Labels for all new images in Hard Negatives
    confusers_dir = BASE / "09_HARD_NEGATIVES_CONFUSERS"
    img_exts = {".jpg", ".jpeg", ".png", ".webp"}
    for root, _, files in os.walk(confusers_dir):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in img_exts:
                lbl = p.with_suffix(".txt")
                if not lbl.exists():
                    lbl.touch()

    print("=" * 60)
    print("ADDITIONAL INGESTION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
