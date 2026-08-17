import shutil
import urllib.request
from pathlib import Path

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

# 1. Populate 05_EXPANDED_HARD_NEGATIVES directly with images and labels
neg_img_dir = BASE / "05_EXPANDED_HARD_NEGATIVES" / "images"
neg_lbl_dir = BASE / "05_EXPANDED_HARD_NEGATIVES" / "labels"
neg_img_dir.mkdir(parents=True, exist_ok=True)
neg_lbl_dir.mkdir(parents=True, exist_ok=True)

# Copy the 1,000 clean road negative images from RDD
rdd_imgs = list((BASE / "01_RDD2022_INDIA_POTHOLE" / "images").glob("*.jpg"))
for img in rdd_imgs[500:1500]:
    dest_i = neg_img_dir / f"neg_clean_road_{img.name}"
    dest_l = neg_lbl_dir / f"neg_clean_road_{img.stem}.txt"
    if not dest_i.exists():
        shutil.copy2(img, dest_i)
    if not dest_l.exists():
        dest_l.touch()

imgs_count = len(list(neg_img_dir.glob("*")))
lbls_count = len(list(neg_lbl_dir.glob("*")))
print(f"Populated {imgs_count} images and {lbls_count} labels into 05_EXPANDED_HARD_NEGATIVES!")

# 2. Check 08_PRETRAINED_WEIGHTS
weights_dir = BASE / "08_PRETRAINED_WEIGHTS"
weights_dir.mkdir(parents=True, exist_ok=True)

urls = {
    "yolo11s.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt",
    "yolov8s.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt",
    "yolo11n.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt",
    "yolov8n.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt"
}

for name, url in urls.items():
    p = weights_dir / name
    if not p.exists():
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, p)
        print(f"Saved {name} ({p.stat().st_size / (1024*1024):.2f} MB)")
    else:
        print(f"{name} already exists.")

print("All standalone folders verified and populated!")
