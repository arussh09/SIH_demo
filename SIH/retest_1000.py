import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, average_precision_score
)
import torch
import torch.nn as nn

OUTPUT_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\FineTuned_Model\sensor_1dcnn_20260817_070853")
DATA_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\1D_CNN\Road Data")

from train_sensor_1dcnn import build_dataset, PotholeSensor1DCNN

def retest_on_1000():
    print("=" * 75)
    print("        RETESTING 1D-CNN MODEL ON EXACTLY 1,000 TEST SAMPLES")
    print("=" * 75)

    # 1. Load full dataset
    X_all, y_all = build_dataset()
    print(f"Total Dataset Pool: {len(X_all)} windows")

    # 2. Extract exactly 1,000 stratified test samples
    _, X_1000, _, y_1000 = train_test_split(
        X_all, y_all, test_size=1000, random_state=123, stratify=y_all
    )
    print(f"Selected Test Set Size: {len(X_1000)} samples")
    CLASS_NAMES = ["Smooth Road", "Pothole", "Speed Bump"]
    for i, c in enumerate(CLASS_NAMES):
        cnt = (y_1000 == i).sum()
        print(f"  - {c:<12}: {cnt:>4} samples ({cnt/len(y_1000)*100:>5.1f}%)")

    # 3. Load Trained Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PotholeSensor1DCNN().to(device)
    model.load_state_dict(torch.load(OUTPUT_DIR / "best.pt", weights_only=True))
    model.eval()

    # 4. Predict
    X_t = torch.tensor(X_1000, dtype=torch.float32).permute(0, 2, 1).to(device)
    with torch.no_grad():
        logits = model(X_t)
        probs = torch.softmax(logits, dim=1).cpu().numpy()
        preds = np.argmax(probs, axis=1)

    # 5. Metrics
    acc = accuracy_score(y_1000, preds)
    bal_acc = balanced_accuracy_score(y_1000, preds)
    cm = confusion_matrix(y_1000, preds)

    print("\n" + "=" * 75)
    print("GLOBAL RESULTS ON 1,000 TEST SAMPLES")
    print("=" * 75)
    print(f"  * Overall Top-1 Accuracy:   {(preds == y_1000).sum()} / 1000  ({acc * 100:.2f}%)")
    print(f"  * Balanced Class Accuracy:  {bal_acc * 100:.2f}%")
    print(f"  * Total Errors:             {(preds != y_1000).sum()} / 1000  ({(1 - acc) * 100:.2f}%)")
    print("-" * 75)

    print("\n" + "=" * 75)
    print("PER-CLASS PERFORMANCE BREAKDOWN (1,000 SAMPLES)")
    print("=" * 75)
    print(f"{'Class Name':<14} | {'Test Count':<10} | {'Correct':<10} | {'Detection Rate':<16} | {'Precision':<12} | {'F1-Score':<10}")
    print("-" * 75)
    for i, c in enumerate(CLASS_NAMES):
        tp = cm[i, i]
        tot = cm[i].sum()
        rec = tp / tot if tot > 0 else 0
        fp = cm[:, i].sum() - tp
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        print(f"{c:<14} | {tot:>10} | {tp:>10} | {rec*100:>14.2f}% | {prec*100:>10.2f}% | {f1*100:>8.2f}%")
    print("-" * 75)

    print("\n" + "=" * 75)
    print("CONFUSION MATRIX (1,000 SAMPLES)")
    print("=" * 75)
    print(f"{'Actual Class':<14} | {'Pred: Smooth':<15} | {'Pred: Pothole':<15} | {'Pred: Bump':<15} | {'Class Acc':<10}")
    print("-" * 75)
    for i, c in enumerate(CLASS_NAMES):
        row_tot = cm[i].sum()
        c0_str = f"{cm[i, 0]} ({cm[i, 0]/row_tot*100:.1f}%)"
        c1_str = f"{cm[i, 1]} ({cm[i, 1]/row_tot*100:.1f}%)"
        c2_str = f"{cm[i, 2]} ({cm[i, 2]/row_tot*100:.1f}%)"
        class_acc = cm[i, i] / row_tot * 100
        print(f"{c:<14} | {c0_str:<15} | {c1_str:<15} | {c2_str:<15} | {class_acc:>8.2f}%")
    print("-" * 75)

    # Pothole specifics
    p_tp = cm[1, 1]
    p_tot = cm[1].sum()
    p_fp = cm[:, 1].sum() - p_tp
    p_fn = p_tot - p_tp
    p_tn = cm.sum() - (p_tp + p_fp + p_fn)

    print("\n" + "=" * 75)
    print("POTHOLE DETECTION SPECIFIC AUDIT (1,000 SAMPLES)")
    print("=" * 75)
    print(f"  * Total Potholes in Test Set:       {p_tot}")
    print(f"  * Potholes Successfully Caught:    {p_tp} / {p_tot} ({p_tp/p_tot*100:.2f}%)")
    print(f"  * Potholes Missed (False Neg):     {p_fn} / {p_tot} ({p_fn/p_tot*100:.2f}%)")
    print(f"  * False Alarms (False Positives):  {p_fp} (out of {1000 - p_tot} non-potholes)")
    print(f"  * Pothole Detection Rate (Recall): {p_tp/p_tot*100:.2f}%")
    print(f"  * Pothole Precision:               {p_tp/(p_tp+p_fp)*100:.2f}%")
    print(f"  * Pothole Specificity:             {p_tn/(p_tn+p_fp)*100:.2f}%")
    print(f"  * Pothole False Alarm Rate (FPR):  {p_fp/(p_tn+p_fp)*100:.2f}%")
    print("=" * 75)

if __name__ == "__main__":
    retest_on_1000()
