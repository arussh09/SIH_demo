import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

OUTPUT_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\FineTuned_Model\sensor_1dcnn_20260817_070853")
DATA_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\1D_CNN\Road Data")

from train_sensor_1dcnn import (
    load_session, extract_windows, PotholeSensor1DCNN,
    NUM_CLASSES, IN_CHANNELS, WINDOW_SIZE, TARGET_HZ
)

def build_dataset_with_session_ids():
    all_windows = []
    all_labels = []
    all_session_ids = []
    
    anomalies_dir = DATA_DIR / "Road Anomalies"
    behaviour_dir = DATA_DIR / "Driving Behaviour"

    session_id = 0
    session_map = {}

    # Potholes
    pothole_sessions = [d for d in sorted(anomalies_dir.iterdir()) if "Pothole" in d.name]
    for s in pothole_sessions:
        sig = load_session(s)
        if sig is None: continue
        w = extract_windows(sig)
        all_windows.append(w)
        all_labels.append(np.full(len(w), 1))
        all_session_ids.append(np.full(len(w), session_id))
        session_map[session_id] = (s.name, "Pothole")
        session_id += 1

    # Bumps
    bump_sessions = [d for d in sorted(anomalies_dir.iterdir()) if "Bump" in d.name]
    for s in bump_sessions:
        sig = load_session(s)
        if sig is None: continue
        w = extract_windows(sig)
        all_windows.append(w)
        all_labels.append(np.full(len(w), 2))
        all_session_ids.append(np.full(len(w), session_id))
        session_map[session_id] = (s.name, "Bump")
        session_id += 1

    # Smooth
    smooth_sessions = list(sorted(behaviour_dir.iterdir()))
    for s in smooth_sessions:
        sig = load_session(s)
        if sig is None: continue
        w = extract_windows(sig)
        all_windows.append(w)
        all_labels.append(np.full(len(w), 0))
        all_session_ids.append(np.full(len(w), session_id))
        session_map[session_id] = (s.name, "Smooth")
        session_id += 1

    X = np.concatenate(all_windows, axis=0)
    y = np.concatenate(all_labels, axis=0)
    groups = np.concatenate(all_session_ids, axis=0)
    return X, y, groups, session_map

def run_strict_session_validation():
    print("=" * 75)
    print("   STRICT REAL-WORLD VALIDATION (LEAVE-SESSIONS-OUT / UNSEEN DRIVES)")
    print("=" * 75)
    
    X, y, groups, session_map = build_dataset_with_session_ids()
    print(f"Total Windows: {len(X)} across {len(session_map)} distinct recording sessions\n")

    # Define held-out sessions that the model has NEVER seen in training
    # Hold out 2 pothole sessions, 2 bump sessions, 2 smooth sessions
    test_session_names = ["15. Pothole", "16. Pothole", "8. Bump", "5. Bump", "4. Standard", "6. Slow"]
    test_session_ids = [sid for sid, (name, _) in session_map.items() if name in test_session_names]
    train_session_ids = [sid for sid in session_map.keys() if sid not in test_session_ids]

    print("HELD-OUT TEST SESSIONS (Completely Unseen Rides):")
    for sid in test_session_ids:
        name, cat = session_map[sid]
        cnt = (groups == sid).sum()
        print(f"  - [{cat:<7}] {name:<20}: {cnt} test windows")

    test_mask = np.isin(groups, test_session_ids)
    train_mask = np.isin(groups, train_session_ids)

    X_train, y_train = X[train_mask], y[train_mask]
    X_test, y_test = X[test_mask], y[test_mask]

    print(f"\nTraining Set:   {len(X_train)} windows (from {len(train_session_ids)} sessions)")
    print(f"Unseen Test Set: {len(X_test)} windows (from {len(test_session_ids)} sessions)")
    print("-" * 75)

    # Train a fresh model on strictly disjoint sessions
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PotholeSensor1DCNN().to(device)

    X_train_t = torch.tensor(X_train, dtype=torch.float32).permute(0, 2, 1)
    y_train_t = torch.tensor(y_train, dtype=torch.long)
    X_test_t = torch.tensor(X_test, dtype=torch.float32).permute(0, 2, 1)
    y_test_t = torch.tensor(y_test, dtype=torch.long)

    train_ds = TensorDataset(X_train_t, y_train_t)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

    class_counts = np.bincount(y_train, minlength=NUM_CLASSES)
    class_weights = 1.0 / np.clip(class_counts, 1, None)
    class_weights = class_weights / class_weights.sum() * NUM_CLASSES
    criterion = nn.CrossEntropyLoss(weight=torch.tensor(class_weights, dtype=torch.float32).to(device))
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

    for epoch in range(40):
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            out = model(xb)
            loss = criterion(out, yb)
            loss.backward()
            optimizer.step()

    # Evaluate on Unseen Sessions
    model.eval()
    with torch.no_grad():
        logits = model(X_test_t.to(device))
        probs = torch.softmax(logits, dim=1).cpu().numpy()
        preds = np.argmax(probs, axis=1)

    acc = accuracy_score(y_test, preds)
    bal_acc = balanced_accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds)

    print("\n" + "=" * 75)
    print("REAL-WORLD ACCURACY ON COMPLETELY UNSEEN DRIVES")
    print("=" * 75)
    print(f"  * Overall Accuracy on Unseen Drives: {acc * 100:.2f}%  ({(preds == y_test).sum()} / {len(y_test)})")
    print(f"  * Balanced Class Accuracy:          {bal_acc * 100:.2f}%")
    print("-" * 75)

    CLASS_NAMES = ["Smooth Road", "Pothole", "Speed Bump"]
    header = "Actual / Pred"
    print(f"{header:<14} | {'Pred: Smooth':<15} | {'Pred: Pothole':<15} | {'Pred: Bump':<15} | {'Class Acc':<10}")
    print("-" * 75)
    for i, c in enumerate(CLASS_NAMES):
        row_tot = cm[i].sum()
        c0_str = f"{cm[i, 0]} ({cm[i, 0]/row_tot*100:.1f}%)" if row_tot > 0 else "0"
        c1_str = f"{cm[i, 1]} ({cm[i, 1]/row_tot*100:.1f}%)" if row_tot > 0 else "0"
        c2_str = f"{cm[i, 2]} ({cm[i, 2]/row_tot*100:.1f}%)" if row_tot > 0 else "0"
        class_acc = cm[i, i] / row_tot * 100 if row_tot > 0 else 0
        print(f"{c:<14} | {c0_str:<15} | {c1_str:<15} | {c2_str:<15} | {class_acc:>8.2f}%")
    print("=" * 75)

if __name__ == "__main__":
    run_strict_session_validation()
