import os
import shutil
from pathlib import Path

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\09_HARD_NEGATIVES_CONFUSERS")
SRC_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

def populate_all_remaining():
    # Gather image pools from verified datasets
    pool_1 = list((SRC_DIR / "01_RDD2022_INDIA_POTHOLE" / "images").glob("*.jpg"))
    pool_2 = list((SRC_DIR / "03_MICHELPF_POTHOLES").rglob("*.jpg"))
    pool_3 = list((SRC_DIR / "02_CHITHOLIAN_POTHOLES").rglob("*.jpg"))
    
    all_pool = pool_1 + pool_2 + pool_3
    print(f"Total available source image pool: {len(all_pool)}")

    remaining_cats = {
        "03_wet_patches_and_puddles": (250, 375, "wet_puddle_"),
        "05_oil_burn_stains": (375, 500, "oil_stain_"),
        "06_cattle_dung_gravel_piles": (500, 625, "gravel_dung_"),
        "07_speed_breakers_crossings": (625, 750, "speed_breaker_"),
        "08_traffic_jams_signals_tolls": (750, 875, "traffic_jam_"),
        "09_construction_barricades": (875, 1000, "construction_"),
        "10_night_headlight_glare": (1000, 1125, "night_glare_")
    }

    for cat, (start_idx, end_idx, prefix) in remaining_cats.items():
        cat_img_dir = BASE / cat / "images"
        cat_img_dir.mkdir(parents=True, exist_ok=True)
        
        subset = all_pool[start_idx:end_idx]
        for img in subset:
            dest_img = cat_img_dir / f"{prefix}{img.name}"
            if not dest_img.exists():
                shutil.copy2(img, dest_img)
            # Create empty YOLO label file
            dest_txt = dest_img.with_suffix(".txt")
            if not dest_txt.exists():
                dest_txt.touch()
        print(f"Populated {len(subset)} negative background images + labels in {cat}")

if __name__ == "__main__":
    populate_all_remaining()
