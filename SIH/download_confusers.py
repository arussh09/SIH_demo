import os
import shutil
from pathlib import Path
import kagglehub
import urllib.request
import zipfile

BASE_CONFUSERS = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\09_HARD_NEGATIVES_CONFUSERS")

def download_and_extract(url, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)
    temp_zip = target_dir / "temp.zip"
    try:
        print(f"Downloading from {url}...")
        urllib.request.urlretrieve(url, temp_zip)
        with zipfile.ZipFile(temp_zip, 'r') as z:
            z.extractall(target_dir)
        temp_zip.unlink()
        print(f"Extracted to {target_dir}")
    except Exception as e:
        print(f"Download failed for {target_dir.name}: {e}")
        if temp_zip.exists():
            temp_zip.unlink()

def ingest_kaggle_dataset(slug, target_subdir):
    dest = BASE_CONFUSERS / target_subdir
    dest.mkdir(parents=True, exist_ok=True)
    try:
        print(f"Fetching {slug} -> {target_subdir}...")
        p = kagglehub.dataset_download(slug)
        shutil.copytree(p, dest, dirs_exist_ok=True)
        print(f"Successfully loaded {slug} into {dest}")
    except Exception as e:
        print(f"Failed {slug}: {e}")

def main():
    print("=" * 60)
    print("DOWNLOADING HARD NEGATIVES & CONFUSERS")
    print("=" * 60)

    # 1. Manholes & Utility Gratings
    print("\n--- [1] Manholes & Gratings ---")
    for s in ["manumishrax/manhole-dataset", "phuctran2002/manhole-for-yolov8", "deeppratapsingh/manhole-detection"]:
        ingest_kaggle_dataset(s, "04_manholes_utility_gratings")
        break

    # 2. Speed Breakers & Crossings
    print("\n--- [2] Speed Breakers & Crossings ---")
    for s in ["balamurugans/yolov5-speed-breaker-detection-driver-alert-system", "sannyshankaran/pothole-and-speed-breaker-detection"]:
        ingest_kaggle_dataset(s, "07_speed_breakers_crossings")
        break

    # 3. Traffic Jams & City Signals
    print("\n--- [3] Traffic Jams & Clean Roads ---")
    for s in ["anmolkumar/traffic-dataset-india", "arnabchaki/indian-traffic-signs-dataset"]:
        ingest_kaggle_dataset(s, "08_traffic_jams_signals_tolls")
        break

    # 4. Construction & Barricades / Cones
    print("\n--- [4] Construction Zones & Cones ---")
    for s in ["sachinpatel21/traffic-cones-dataset", "tungdop/traffic-cone-detection"]:
        ingest_kaggle_dataset(s, "09_construction_barricades")
        break

    # 5. Night Road & Glare
    print("\n--- [5] Night Driving & Glare ---")
    for s in ["solesensei/nighttime-scene-parsing", "subhamg/night-road-image-dataset"]:
        ingest_kaggle_dataset(s, "10_night_headlight_glare")
        break

    # 6. Stray Cattle on Road
    print("\n--- [6] Cattle / Obstacles on Road ---")
    for s in ["alxmamaev/cow-images", "ayushkh/cattle-detection"]:
        ingest_kaggle_dataset(s, "06_cattle_dung_gravel_piles")
        break

    # 7. Wet Asphalt & Puddles / Reflections
    print("\n--- [7] Wet Road & Puddles ---")
    for s in ["prasadperera/puddle-detection-dataset", "salmankhaliq22/wet-road-dataset"]:
        ingest_kaggle_dataset(s, "03_wet_patches_and_puddles")
        break

    # 8. Shadows & Tar Patches
    print("\n--- [8] Shadows & Tar Patches ---")
    for s in ["kshitijdhama/road-damage-detection", "adrianludwicki/rdd2022es"]:
        ingest_kaggle_dataset(s, "01_tar_patches_and_bitumen")
        ingest_kaggle_dataset(s, "02_shadows_trees_vehicles")
        break

    print("\n" + "=" * 60)
    print("CONFUSERS DOWNLOAD PIPELINE FINISHED")
    print("=" * 60)

if __name__ == "__main__":
    main()
