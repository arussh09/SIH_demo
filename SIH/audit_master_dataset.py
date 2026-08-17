import os
import hashlib
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

def compute_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def audit_dataset():
    print("=" * 70)
    print("UNIFIED MASTER DATASET QUALITY AUDIT")
    print("=" * 70)

    img_exts = {".jpg", ".jpeg", ".png", ".webp"}
    all_images = []
    
    for root, _, files in os.walk(BASE):
        # Exclude pre-trained weights folder from image audit
        if "08_PRETRAINED_WEIGHTS" in root or ".git" in root:
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in img_exts:
                all_images.append(p)
                
    print(f"Total Images Found Across All Folders: {len(all_images)}")

    # 1. Deduplication & Corruption Check
    seen_hashes = {}
    duplicates = []
    corrupted = []
    resolutions = {}
    
    print("\nScanning images for integrity, resolution, and duplicates...")
    for idx, img_p in enumerate(all_images):
        if idx % 1000 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(all_images)} images...")
        try:
            h = compute_hash(img_p)
            if h in seen_hashes:
                duplicates.append((img_p, seen_hashes[h]))
            else:
                seen_hashes[h] = img_p
                
            with Image.open(img_p) as im:
                w, h_dim = im.size
                res_bucket = f"{w}x{h_dim}"
                resolutions[res_bucket] = resolutions.get(res_bucket, 0) + 1
        except Exception as e:
            corrupted.append((img_p, str(e)))

    print(f"\nAudit Summary:")
    print(f"  - Total Unique Images: {len(seen_hashes)}")
    print(f"  - Duplicate Images: {len(duplicates)}")
    print(f"  - Corrupted Images: {len(corrupted)}")
    
    print("\nTop 8 Image Resolutions:")
    for res, count in sorted(resolutions.items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"    * {res:<15}: {count} images ({count/len(all_images)*100:.1f}%)")

if __name__ == "__main__":
    audit_dataset()
