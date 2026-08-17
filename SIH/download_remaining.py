import os
import shutil
import urllib.request
import zipfile
from pathlib import Path
import kagglehub

BASE_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

def download_and_extract_zip(url, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "temp.zip"
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, zip_path)
    print(f"Extracting {zip_path} to {dest_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
    zip_path.unlink()
    print(f"Extraction complete for {dest_dir.name}!")

def fix_rad_bengaluru():
    print("Fixing 06_RAD_BENGALURU_SPRINGER...")
    dest = BASE_DIR / "06_RAD_BENGALURU_SPRINGER"
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    url = "https://github.com/oracl4/RoadDamageDetection/archive/refs/heads/main.zip"
    try:
        download_and_extract_zip(url, dest)
    except Exception as e:
        print(f"Error downloading RAD: {e}")

def fix_roboflow_benchmark():
    print("Downloading 05_ROBOFLOW_POTHOLE_BENCHMARK...")
    dest = BASE_DIR / "05_ROBOFLOW_POTHOLE_BENCHMARK"
    dest.mkdir(exist_ok=True)
    try:
        path = kagglehub.dataset_download("sovitrath/pothole-detection-dataset-yolov8")
        shutil.copytree(path, dest, dirs_exist_ok=True)
        print(f"Downloaded Roboflow/Sovit Pothole benchmark to {dest}")
    except Exception as e:
        print(f"Kagglehub error: {e}")

def fix_miia_potholes():
    print("Downloading 04_MIIA_AFRICA_POTHOLES...")
    dest = BASE_DIR / "04_MIIA_AFRICA_POTHOLES"
    dest.mkdir(exist_ok=True)
    try:
        path = kagglehub.dataset_download("bhanupratapbiswas/pothole-detection-dataset")
        shutil.copytree(path, dest, dirs_exist_ok=True)
        print(f"Downloaded Pothole dataset to {dest}")
    except Exception as e:
        print(f"Kagglehub error: {e}")

if __name__ == "__main__":
    fix_rad_bengaluru()
    fix_roboflow_benchmark()
    fix_miia_potholes()
    print("All remaining fixes finished!")
