import os
from pathlib import Path

BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS")

def count_files(directory):
    img_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    label_exts = {".txt", ".xml", ".json"}
    
    img_count = 0
    label_count = 0
    total_size = 0
    
    for root, _, files in os.walk(directory):
        for f in files:
            p = Path(root) / f
            total_size += p.stat().st_size
            ext = p.suffix.lower()
            if ext in img_exts:
                img_count += 1
            elif ext in label_exts:
                label_count += 1
                
    return img_count, label_count, total_size / (1024*1024)

print("=" * 70)
print(f"{'Folder Name':<35} | {'Images':<8} | {'Labels':<8} | {'Size (MB)':<10}")
print("-" * 70)

for item in sorted(BASE.iterdir()):
    if item.is_dir():
        imgs, labels, size_mb = count_files(item)
        print(f"{item.name:<35} | {imgs:<8} | {labels:<8} | {size_mb:<10.1f}")

print("=" * 70)
