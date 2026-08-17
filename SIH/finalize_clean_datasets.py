import os
import shutil
import xml.etree.ElementTree as ET
import random
from pathlib import Path
from PIL import Image

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")
UNIFIED_DIR = BASE / "unified_yolo11_potholes"

def convert_xml_to_yolo(xml_file, img_w, img_h, target_class_id=0):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        yolo_lines = []
        
        for obj in root.findall('object'):
            b = obj.find('bndbox')
            if b is None:
                continue
            xmin = float(b.find('xmin').text)
            xmax = float(b.find('xmax').text)
            ymin = float(b.find('ymin').text)
            ymax = float(b.find('ymax').text)
            
            xmin = max(0.0, min(xmin, img_w))
            xmax = max(0.0, min(xmax, img_w))
            ymin = max(0.0, min(ymin, img_h))
            ymax = max(0.0, min(ymax, img_h))
            
            bw = xmax - xmin
            bh = ymax - ymin
            if bw <= 1 or bh <= 1:
                continue
                
            xc = (xmin + bw / 2.0) / img_w
            yc = (ymin + bh / 2.0) / img_h
            wn = bw / img_w
            hn = bh / img_h
            
            yolo_lines.append(f"{target_class_id} {xc:.6f} {yc:.6f} {wn:.6f} {hn:.6f}\n")
            
        return yolo_lines
    except Exception as e:
        return []

def main():
    print("=" * 60)
    print("ASSEMBLING MASTER 4,971-IMAGE UNIFIED YOLO11 DATASET")
    print("=" * 60)
    
    train_img_dir = UNIFIED_DIR / "train" / "images"
    train_lbl_dir = UNIFIED_DIR / "train" / "labels"
    val_img_dir = UNIFIED_DIR / "val" / "images"
    val_lbl_dir = UNIFIED_DIR / "val" / "labels"
    
    if UNIFIED_DIR.exists():
        shutil.rmtree(UNIFIED_DIR, ignore_errors=True)
        
    for d in [train_img_dir, train_lbl_dir, val_img_dir, val_lbl_dir]:
        d.mkdir(parents=True, exist_ok=True)
        
    all_pairs = []
    
    # 1. RDD2022 India Potholes (1,530 images)
    rdd_dir = BASE / "01_RDD2022_INDIA_POTHOLE"
    rdd_imgs = list((rdd_dir / "images").glob("*.jpg"))
    for img_p in rdd_imgs:
        xml_p = rdd_dir / "annotations" / "xmls" / f"{img_p.stem}.xml"
        if xml_p.exists():
            with Image.open(img_p) as im:
                w, h = im.size
            lines = convert_xml_to_yolo(xml_p, w, h, target_class_id=0)
            all_pairs.append((img_p, lines, f"rdd_{img_p.stem}"))
    print(f"Loaded {len(rdd_imgs)} pairs from RDD2022 India.")

    # 2. Chitholian Potholes (665 images from annotated-images)
    chith_dir = BASE / "02_CHITHOLIAN_POTHOLES"
    chith_imgs = list(chith_dir.rglob("*.jpg")) + list(chith_dir.rglob("*.png"))
    chith_loaded = 0
    for img_p in chith_imgs:
        xml_p = img_p.with_suffix(".xml")
        if xml_p.exists():
            with Image.open(img_p) as im:
                w, h = im.size
            lines = convert_xml_to_yolo(xml_p, w, h, target_class_id=0)
            all_pairs.append((img_p, lines, f"chith_{img_p.stem}"))
            chith_loaded += 1
    print(f"Loaded {chith_loaded} pairs from Chitholian Potholes.")

    # 3. MichelPF YOLO Potholes (1,983 images)
    michel_dir = BASE / "03_MICHELPF_POTHOLES"
    michel_imgs = list(michel_dir.rglob("*.jpg"))
    michel_loaded = 0
    for img_p in michel_imgs:
        txt_p = img_p.with_suffix(".txt")
        if txt_p.exists():
            with open(txt_p, 'r') as f:
                lines = f.readlines()
            all_pairs.append((img_p, lines, f"michel_{img_p.stem}"))
            michel_loaded += 1
    print(f"Loaded {michel_loaded} pairs from MichelPF.")

    # 4. Manholes & Drain Covers (793 background negatives)
    manhole_dir = BASE / "04_MANHOLES_AND_DRAIN_COVERS"
    manhole_imgs = list(manhole_dir.rglob("*.jpg")) + list(manhole_dir.rglob("*.png"))
    for img_p in manhole_imgs:
        all_pairs.append((img_p, [], f"manhole_{img_p.stem}"))
    print(f"Loaded {len(manhole_imgs)} negative background pairs from Manholes & Covers.")

    print(f"\nGRAND TOTAL VERIFIED IMAGE-LABEL PAIRS: {len(all_pairs)}")

    # Shuffle and Split (80% Train, 20% Val)
    random.seed(42)
    random.shuffle(all_pairs)
    
    split_idx = int(len(all_pairs) * 0.8)
    train_pairs = all_pairs[:split_idx]
    val_pairs = all_pairs[split_idx:]
    
    print(f"Writing {len(train_pairs)} Train pairs and {len(val_pairs)} Validation pairs to disk...")
    
    for img_p, lines, base_name in train_pairs:
        dest_img = train_img_dir / f"{base_name}{img_p.suffix}"
        dest_lbl = train_lbl_dir / f"{base_name}.txt"
        shutil.copy2(img_p, dest_img)
        with open(dest_lbl, 'w') as f:
            f.writelines(lines)
            
    for img_p, lines, base_name in val_pairs:
        dest_img = val_img_dir / f"{base_name}{img_p.suffix}"
        dest_lbl = val_lbl_dir / f"{base_name}.txt"
        shutil.copy2(img_p, dest_img)
        with open(dest_lbl, 'w') as f:
            f.writelines(lines)

    # Generate data.yaml
    path_posix = UNIFIED_DIR.as_posix()
    yaml_content = f"""# YOLO11 Pothole Detection Dataset Configuration
path: {path_posix}
train: train/images
val: val/images

# Classes
nc: 1
names: ['pothole']
"""
    yaml_file = UNIFIED_DIR / "data.yaml"
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
        
    print(f"\nGenerated {yaml_file} successfully!")
    print("=" * 60)
    print("MASTER UNIFIED DATASET ASSEMBLED AND READY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
