import os
import shutil
import subprocess
import urllib.request
import kagglehub
from pathlib import Path

BASE_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")
BASE_DIR.mkdir(parents=True, exist_ok=True)

def print_banner(msg):
    print("\n" + "=" * 60)
    print(f"  {msg}")
    print("=" * 60)

def download_file(url, dest_path):
    print(f"Downloading {url} -> {dest_path}...")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest_path)
    print(f"Saved {dest_path.name} ({os.path.getsize(dest_path) / (1024*1024):.2f} MB)")

# 1. RDD2022 India Pothole
def setup_rdd2022_india():
    print_banner("1. Setting up 01_RDD2022_INDIA_POTHOLE")
    dest = BASE_DIR / "01_RDD2022_INDIA_POTHOLE"
    dest.mkdir(exist_ok=True)
    cache_path = Path(r"C:\Users\Jaina\.cache\kagglehub\datasets\vidishbijalwan\rdd2022-india-pothole-d40\versions\1\train")
    if cache_path.exists():
        for item in cache_path.iterdir():
            target = dest / item.name
            if not target.exists():
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
        print(f"Successfully copied RDD2022 India dataset to {dest}")
    else:
        path = kagglehub.dataset_download("vidishbijalwan/rdd2022-india-pothole-d40")
        shutil.copytree(path, dest, dirs_exist_ok=True)
        print(f"Downloaded and copied to {dest}")

# 2. Chitholian Potholes Dataset
def setup_chitholian():
    print_banner("2. Downloading 02_CHITHOLIAN_POTHOLES")
    dest = BASE_DIR / "02_CHITHOLIAN_POTHOLES"
    dest.mkdir(exist_ok=True)
    try:
        path = kagglehub.dataset_download("chitholian/annotated-potholes-dataset")
        shutil.copytree(path, dest, dirs_exist_ok=True)
        print(f"Downloaded Chitholian dataset to {dest}")
    except Exception as e:
        print(f"Error downloading Chitholian dataset: {e}")

# 3. MichelPF Potholes Dataset (GitHub YOLO annotated)
def setup_michelpf():
    print_banner("3. Downloading 03_MICHELPF_POTHOLES")
    dest = BASE_DIR / "03_MICHELPF_POTHOLES"
    dest.mkdir(exist_ok=True)
    repo_url = "https://github.com/michelpf/dataset-pothole.git"
    if not (dest / "README.md").exists():
        try:
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(dest)], check=True)
            print(f"Cloned MichelPF dataset into {dest}")
        except Exception as e:
            print(f"Git clone error: {e}")
    else:
        print(f"MichelPF dataset already exists at {dest}")

# 4. MIIA Africa Potholes
def setup_miia_africa():
    print_banner("4. Downloading 04_MIIA_AFRICA_POTHOLES")
    dest = BASE_DIR / "04_MIIA_AFRICA_POTHOLES"
    dest.mkdir(exist_ok=True)
    try:
        path = kagglehub.dataset_download("atillaciga/miia-pothole-image-classification-challenge")
        shutil.copytree(path, dest, dirs_exist_ok=True)
        print(f"Downloaded MIIA Africa dataset to {dest}")
    except Exception as e:
        print(f"Kagglehub error: {e}")

# 5. Roboflow Universe Potholes Benchmark
def setup_roboflow_potholes():
    print_banner("5. Downloading 05_ROBOFLOW_POTHOLE_BENCHMARK")
    dest = BASE_DIR / "05_ROBOFLOW_POTHOLE_BENCHMARK"
    dest.mkdir(exist_ok=True)
    try:
        path = kagglehub.dataset_download("sanketparab/pothole-detection-dataset-using-yolo")
        shutil.copytree(path, dest, dirs_exist_ok=True)
        print(f"Downloaded Roboflow/YOLO Pothole dataset to {dest}")
    except Exception as e:
        print(f"Kagglehub error: {e}")

# 6. RAD Bengaluru & Springer Research Tools
def setup_rad_bengaluru():
    print_banner("6. Setting up 06_RAD_BENGALURU_SPRINGER")
    dest = BASE_DIR / "06_RAD_BENGALURU_SPRINGER"
    dest.mkdir(exist_ok=True)
    repo_url = "https://github.com/oracl4/RoadDamageDetection.git"
    if not (dest / "README.md").exists():
        try:
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(dest)], check=True)
            print(f"Cloned RAD / Road Damage tools into {dest}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Already exists at {dest}")

# 7. Pretrained Weights
def setup_pretrained_weights():
    print_banner("7. Downloading 08_PRETRAINED_WEIGHTS")
    dest = BASE_DIR / "08_PRETRAINED_WEIGHTS"
    dest.mkdir(exist_ok=True)
    
    weights = {
        "yolov8s.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt",
        "yolo11s.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt",
        "yolov8n.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt",
        "yolo11n.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt"
    }
    for name, url in weights.items():
        file_path = dest / name
        if not file_path.exists():
            download_file(url, file_path)
        else:
            print(f"{name} already exists.")

# 8. Hard Negatives & Confusers Folders
def setup_hard_negatives():
    print_banner("8. Structuring 09_HARD_NEGATIVES_CONFUSERS")
    confusers_dir = BASE_DIR / "09_HARD_NEGATIVES_CONFUSERS"
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
        cat_path = confusers_dir / cat
        cat_path.mkdir(parents=True, exist_ok=True)
        readme = cat_path / "README.md"
        if not readme.exists():
            readme.write_text(f"# Confuser Category: {cat}\n\n"
                              f"Negative background images containing {cat.replace('_', ' ')}.\n"
                              f"When fed to YOLO, these images should have corresponding empty .txt label files "
                              f"to explicitly train the model to suppress false positive pothole detections.\n")
    print(f"Created all 10 hard-negative confuser directories in {confusers_dir}")

def main():
    print_banner("STARTING DATASET INGESTION PIPELINE")
    print(f"Target Directory: {BASE_DIR}\n")
    
    setup_rdd2022_india()
    setup_chitholian()
    setup_michelpf()
    setup_miia_africa()
    setup_roboflow_potholes()
    setup_rad_bengaluru()
    setup_pretrained_weights()
    setup_hard_negatives()
    
    print_banner("DATASET INGESTION COMPLETE")

if __name__ == "__main__":
    main()
