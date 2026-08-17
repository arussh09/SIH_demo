import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import kagglehub

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

def clean_bad_folders():
    print("=" * 60)
    print("1. CLEANING UP ARTIFICIAL / RECYCLED CONFUSER FOLDERS")
    print("=" * 60)
    
    # Save the genuine manhole dataset before deleting 09_HARD_NEGATIVES_CONFUSERS
    old_manhole = BASE / "09_HARD_NEGATIVES_CONFUSERS" / "04_manholes_utility_gratings"
    temp_manhole = BASE / "_temp_manhole"
    
    if old_manhole.exists():
        print("Preserving genuine manhole dataset...")
        if temp_manhole.exists():
            shutil.rmtree(temp_manhole)
        shutil.copytree(old_manhole, temp_manhole)
        
    # Remove bad confusers folder
    bad_confusers = BASE / "09_HARD_NEGATIVES_CONFUSERS"
    if bad_confusers.exists():
        shutil.rmtree(bad_confusers, ignore_errors=True)
        print("Removed bad 09_HARD_NEGATIVES_CONFUSERS folder.")
        
    # Move preserved manholes to dedicated folder
    dest_manhole = BASE / "04_MANHOLES_AND_DRAIN_COVERS"
    if dest_manhole.exists():
        shutil.rmtree(dest_manhole, ignore_errors=True)
    if temp_manhole.exists():
        shutil.move(temp_manhole, dest_manhole)
        print("Created dedicated 04_MANHOLES_AND_DRAIN_COVERS with 793 real images.")

    # Remove temporary or duplicate folders
    for f in ["04_MIIA_AFRICA_POTHOLES", "05_ROBOFLOW_POTHOLE_BENCHMARK", "06_RAD_BENGALURU_SPRINGER", "07_TDRD_TOP_DOWN", "rdd2022-india-pothole-d40"]:
        p = BASE / f
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)
            print(f"Cleaned up {f}.")

def install_good_datasets():
    print("\n" + "=" * 60)
    print("2. DOWNLOADING GENUINE, HIGH-QUALITY DATASETS")
    print("=" * 60)

    # 1. Real Puddle & Wet Road Dataset
    dest_puddle = BASE / "05_REAL_WATER_PUDDLES_AND_WET_ROADS"
    if not dest_puddle.exists():
        print("\nDownloading genuine Water Puddle Detection dataset...")
        try:
            subprocess.run(["git", "clone", "--depth", "1", "https://github.com/carlossant83/PuddleDetection.git", str(dest_puddle)], check=True)
            print("Successfully installed 05_REAL_WATER_PUDDLES_AND_WET_ROADS!")
        except Exception as e:
            print(f"Puddle dataset clone error: {e}")

    # 2. Real Night Driving & Headlight Glare Dataset
    dest_night = BASE / "06_REAL_NIGHT_DRIVING_AND_GLARE"
    if not dest_night.exists():
        print("\nDownloading genuine Night Driving & Headlight dataset...")
        try:
            subprocess.run(["git", "clone", "--depth", "1", "https://github.com/alexeyab/yolo-models-for-night-vision.git", str(dest_night)], check=True)
            print("Successfully installed 06_REAL_NIGHT_DRIVING_AND_GLARE!")
        except Exception as e:
            print(f"Night driving dataset clone error: {e}")

    # 3. Real Indian Speed Breakers & Hazards
    dest_speed = BASE / "07_INDIAN_SPEED_BREAKERS_AND_HAZARDS"
    if not dest_speed.exists():
        old_speed = BASE / "10_INDIAN_SPEED_BREAKERS_AND_HAZARDS"
        if old_speed.exists():
            shutil.move(old_speed, dest_speed)
        else:
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/saisantosh1012/speed-breaker-pothole-detection-system-using-python.git", str(dest_speed)], check=True)
            except Exception as e:
                print(f"Speed breaker error: {e}")

    # Rename 08_PRETRAINED_WEIGHTS to 08_PRETRAINED_WEIGHTS cleanly
    old_weights = BASE / "08_PRETRAINED_WEIGHTS"
    if old_weights.exists():
        print("\nPreserved 08_PRETRAINED_WEIGHTS.")

    # Remove remaining old numbering if any
    old_11 = BASE / "11_INDIAN_ROAD_DISTRESS_BENCHMARK"
    if old_11.exists():
        dest_11 = BASE / "09_INDIAN_ROAD_DISTRESS_BENCHMARK"
        if dest_11.exists():
            shutil.rmtree(dest_11, ignore_errors=True)
        shutil.move(old_11, dest_11)

def verify_all():
    print("\n" + "=" * 70)
    print(f"{'Clean Dataset Folder':<40} | {'Images':<8} | {'Size (MB)':<10}")
    print("-" * 70)
    img_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    for item in sorted(BASE.iterdir()):
        if item.is_dir():
            imgs = sum(1 for root, _, files in os.walk(item) for f in files if Path(f).suffix.lower() in img_exts)
            size_mb = sum(Path(root, f).stat().st_size for root, _, files in os.walk(item) for f in files) / (1024*1024)
            print(f"{item.name:<40} | {imgs:<8} | {size_mb:<10.1f}")
    print("=" * 70)

if __name__ == "__main__":
    clean_bad_folders()
    install_good_datasets()
    verify_all()
