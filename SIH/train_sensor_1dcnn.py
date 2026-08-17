"""
SETU -- 1D-CNN Sensor Model Training Pipeline
=============================================
Trains the on-device pothole detection model (Model 1) from labeled IMU data.

Dataset:  Nature Scientific Data smartphone sensor recordings
          - Road Anomalies: "X. Pothole" and "X. Bump" sessions
          - Driving Behaviour: "X. Aggressive/Standard/Slow" sessions (smooth road)

Classes:  0 = smooth_road,  1 = pothole,  2 = bump
Output:   PyTorch .pt, ONNX .onnx, and quantised INT8 ONNX

Hardware: RTX 4060 Laptop GPU -- trains in < 2 minutes.
"""

import os
import json
import shutil
import warnings
import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from scipy.signal import butter, sosfiltfilt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

warnings.filterwarnings("ignore")

# ===================================================================
# CONFIGURATION
# ===================================================================
DATA_DIR = Path(r"D:\HelloWorld\PROJECTS\SIH2026\DATASETS\1D_CNN\Road Data")
OUTPUT_BASE = Path(r"D:\HelloWorld\PROJECTS\SIH2026\FineTuned_Model")

WINDOW_SEC = 2.0           # 2-second sliding window (per PROJECT.md S12.1)
OVERLAP = 0.5              # 50% overlap
TARGET_HZ = 100            # resample all sessions to 100 Hz
WINDOW_SIZE = int(WINDOW_SEC * TARGET_HZ)  # 200 timesteps

# Bandpass filter: 0.5-30 Hz (per PROJECT.md S12.1 step [4])
BANDPASS_LOW = 0.5
BANDPASS_HIGH = 30.0

NUM_CLASSES = 3            # smooth_road=0, pothole=1, bump=2
IN_CHANNELS = 6            # accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z

# Training hyperparameters
EPOCHS = 80
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1e-4
PATIENCE = 15              # early stopping


# ===================================================================
# SIGNAL PROCESSING  (following PROJECT.md S12.1 chain)
# ===================================================================

def resample_to_fixed_hz(df, target_hz=TARGET_HZ):
    """Step [1]: Resample to fixed 100 Hz grid by linear interpolation."""
    t = df["seconds_elapsed"].values
    t_start, t_end = t[0], t[-1]
    n_samples = int((t_end - t_start) * target_hz)
    if n_samples < WINDOW_SIZE:
        return None
    t_new = np.linspace(t_start, t_end, n_samples)
    resampled = {"seconds_elapsed": t_new}
    for col in ["x", "y", "z"]:
        resampled[col] = np.interp(t_new, t, df[col].values)
    return pd.DataFrame(resampled)


def apply_orientation_correction(accel_df, gravity_df):
    """
    Step [2]: Orientation correction using gravity vector.
    Projects raw accel into vehicle frame: a_vertical, a_longitudinal, a_lateral.
    Simplified version: subtract gravity to get dynamic acceleration,
    then use gravity direction to define vertical axis.
    """
    # Resample gravity to match accel timestamps
    grav_resampled = resample_to_fixed_hz(gravity_df)
    acc_resampled = resample_to_fixed_hz(accel_df)

    if grav_resampled is None or acc_resampled is None:
        return None

    # Align lengths
    min_len = min(len(acc_resampled), len(grav_resampled))
    acc_resampled = acc_resampled.iloc[:min_len].reset_index(drop=True)
    grav_resampled = grav_resampled.iloc[:min_len].reset_index(drop=True)

    # Raw accel and gravity vectors
    a = acc_resampled[["x", "y", "z"]].values  # (N, 3)
    g = grav_resampled[["x", "y", "z"]].values  # (N, 3)

    # Step [3]: Gravity removal -> dynamic acceleration
    a_dynamic = a - g

    # Project dynamic accel onto gravity direction (vertical component)
    g_norm = np.linalg.norm(g, axis=1, keepdims=True)
    g_unit = g / np.clip(g_norm, 1e-6, None)

    # Vertical = component along gravity
    a_vert = np.sum(a_dynamic * g_unit, axis=1, keepdims=True)

    # Horizontal plane = remove vertical component
    a_horiz = a_dynamic - a_vert * g_unit

    # Use x and y of horizontal as longitudinal and lateral (approximate)
    result = pd.DataFrame({
        "seconds_elapsed": acc_resampled["seconds_elapsed"].values,
        "a_vert": a_vert.flatten(),
        "a_long": a_horiz[:, 0],
        "a_lat": a_horiz[:, 1],
    })
    return result


def bandpass_filter(signal, fs=TARGET_HZ, low=BANDPASS_LOW, high=BANDPASS_HIGH, order=4):
    """Step [4]: Bandpass 0.5-30 Hz."""
    nyq = fs / 2.0
    low_n = low / nyq
    high_n = high / nyq
    # Clamp to valid range
    low_n = max(low_n, 0.001)
    high_n = min(high_n, 0.999)
    sos = butter(order, [low_n, high_n], btype="band", output="sos")
    return sosfiltfilt(sos, signal, axis=0)


def normalize_per_session(data):
    """Step [5]: Per-device normalisation (z-score per session)."""
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    std[std < 1e-6] = 1e-6
    return (data - mean) / std


# ===================================================================
# DATA LOADING
# ===================================================================

def load_session(session_dir):
    """Load and preprocess a single recording session."""
    acc_path = session_dir / "Accelerometer.csv"
    gyro_path = session_dir / "Gyroscope.csv"
    grav_path = session_dir / "Gravity.csv"

    if not all(p.exists() for p in [acc_path, gyro_path, grav_path]):
        return None

    acc_df = pd.read_csv(acc_path)
    gyro_df = pd.read_csv(gyro_path)
    grav_df = pd.read_csv(grav_path)

    # Step [1-3]: Resample + orientation correction + gravity removal
    corrected = apply_orientation_correction(acc_df, grav_df)
    if corrected is None:
        return None

    gyro_resampled = resample_to_fixed_hz(gyro_df)
    if gyro_resampled is None:
        return None

    # Align lengths
    min_len = min(len(corrected), len(gyro_resampled))
    if min_len < WINDOW_SIZE:
        return None

    corrected = corrected.iloc[:min_len].reset_index(drop=True)
    gyro_resampled = gyro_resampled.iloc[:min_len].reset_index(drop=True)

    # Build 6-channel signal: [a_vert, a_long, a_lat, gyro_x, gyro_y, gyro_z]
    signal = np.column_stack([
        corrected[["a_vert", "a_long", "a_lat"]].values,
        gyro_resampled[["x", "y", "z"]].values,
    ])

    # Step [4]: Bandpass filter each channel
    filtered = bandpass_filter(signal, fs=TARGET_HZ)

    # Step [5]: Per-session normalisation
    normalized = normalize_per_session(filtered)

    return normalized


def extract_windows(signal, window_size=WINDOW_SIZE, overlap=OVERLAP):
    """Step [6]: Sliding window extraction with overlap."""
    step = int(window_size * (1.0 - overlap))
    windows = []
    for start in range(0, len(signal) - window_size + 1, step):
        window = signal[start : start + window_size]
        windows.append(window)
    return np.array(windows) if windows else np.empty((0, window_size, signal.shape[1]))


def build_dataset():
    """Load all sessions, extract windows, assign labels."""
    all_windows = []
    all_labels = []

    anomalies_dir = DATA_DIR / "Road Anomalies"
    behaviour_dir = DATA_DIR / "Driving Behaviour"

    # --- POTHOLE sessions (label = 1) ---
    pothole_sessions = [d for d in sorted(anomalies_dir.iterdir()) if "Pothole" in d.name]
    print(f"  Found {len(pothole_sessions)} Pothole sessions")
    for session_dir in pothole_sessions:
        signal = load_session(session_dir)
        if signal is None:
            print(f"    [X] Skipped {session_dir.name} (too short or missing files)")
            continue
        windows = extract_windows(signal)
        all_windows.append(windows)
        all_labels.append(np.full(len(windows), 1))  # pothole = 1
        print(f"    [OK] {session_dir.name}: {len(windows)} windows")

    # --- BUMP sessions (label = 2) ---
    bump_sessions = [d for d in sorted(anomalies_dir.iterdir()) if "Bump" in d.name]
    print(f"  Found {len(bump_sessions)} Bump sessions")
    for session_dir in bump_sessions:
        signal = load_session(session_dir)
        if signal is None:
            print(f"    [X] Skipped {session_dir.name} (too short or missing files)")
            continue
        windows = extract_windows(signal)
        all_windows.append(windows)
        all_labels.append(np.full(len(windows), 2))  # bump = 2
        print(f"    [OK] {session_dir.name}: {len(windows)} windows")

    # --- SMOOTH ROAD sessions (label = 0) from Driving Behaviour ---
    smooth_sessions = list(sorted(behaviour_dir.iterdir()))
    print(f"  Found {len(smooth_sessions)} Smooth Road / Driving Behaviour sessions")
    for session_dir in smooth_sessions:
        signal = load_session(session_dir)
        if signal is None:
            print(f"    [X] Skipped {session_dir.name} (too short or missing files)")
            continue
        windows = extract_windows(signal)
        all_windows.append(windows)
        all_labels.append(np.full(len(windows), 0))  # smooth = 0
        print(f"    [OK] {session_dir.name}: {len(windows)} windows")

    X = np.concatenate(all_windows, axis=0)  # (N, 200, 6)
    y = np.concatenate(all_labels, axis=0)   # (N,)

    return X, y


# ===================================================================
# MODEL ARCHITECTURE  (per PROJECT.md S12.3)
# ===================================================================

class PotholeSensor1DCNN(nn.Module):
    """
    1D-CNN for road surface classification from 6-axis IMU data.

    Architecture from PROJECT.md S12.3:
      Conv1D(32, k=7, stride=2) -> BN -> ReLU
      Conv1D(64, k=5)           -> BN -> ReLU -> MaxPool(2)
      Conv1D(64, k=3)           -> BN -> ReLU
      GlobalAveragePooling1D
      Dense(32) -> Dropout(0.3) -> Dense(num_classes, softmax)

    Input:  (batch, 6, 200)  -> 6 channels, 200 timesteps
    Output: (batch, num_classes) logits
    """

    def __init__(self, num_classes=NUM_CLASSES, in_channels=IN_CHANNELS):
        super().__init__()
        self.conv_block = nn.Sequential(
            nn.Conv1d(in_channels, 32, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(inplace=True),

            nn.Conv1d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2),

            nn.Conv1d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),

            nn.AdaptiveAvgPool1d(1),  # Global Average Pooling
        )
        self.classifier = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes),
        )

    def forward(self, x):
        # x: (batch, channels, seq_len) -> e.g. (B, 6, 200)
        feat = self.conv_block(x)      # -> (B, 64, 1)
        feat = feat.squeeze(-1)        # -> (B, 64)
        return self.classifier(feat)   # -> (B, num_classes)


# ===================================================================
# TRAINING LOOP
# ===================================================================

def train_model(X_train, y_train, X_val, y_val, output_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n  Device: {device}", end="")
    if device.type == "cuda":
        print(f" ({torch.cuda.get_device_name(0)})")
    else:
        print()

    model = PotholeSensor1DCNN().to(device)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Parameters: {total_params:,} total, {trainable_params:,} trainable")

    # Transpose: (N, 200, 6) -> (N, 6, 200) for Conv1d
    X_train_t = torch.tensor(X_train, dtype=torch.float32).permute(0, 2, 1)
    y_train_t = torch.tensor(y_train, dtype=torch.long)
    X_val_t = torch.tensor(X_val, dtype=torch.float32).permute(0, 2, 1)
    y_val_t = torch.tensor(y_val, dtype=torch.long)

    train_ds = TensorDataset(X_train_t, y_train_t)
    val_ds = TensorDataset(X_val_t, y_val_t)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, pin_memory=True)

    # Class weights to handle imbalance (PROJECT.md S12.4)
    class_counts = np.bincount(y_train, minlength=NUM_CLASSES)
    class_weights = 1.0 / np.clip(class_counts, 1, None)
    class_weights = class_weights / class_weights.sum() * NUM_CLASSES
    weights_tensor = torch.tensor(class_weights, dtype=torch.float32).to(device)
    print(f"  Class weights: {dict(zip(['smooth','pothole','bump'], class_weights.round(3)))}")

    criterion = nn.CrossEntropyLoss(weight=weights_tensor)
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)

    best_val_acc = 0.0
    best_val_loss = float("inf")
    patience_counter = 0
    history = {"epoch": [], "train_loss": [], "train_acc": [], "val_loss": [], "val_acc": [], "lr": []}

    print(f"\n{'Epoch':>6} {'Train Loss':>11} {'Train Acc':>10} {'Val Loss':>10} {'Val Acc':>9} {'LR':>10}")
    print("-" * 62)

    for epoch in range(1, EPOCHS + 1):
        # -- Train --
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            logits = model(x_batch)
            loss = criterion(logits, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(y_batch)
            train_correct += (logits.argmax(1) == y_batch).sum().item()
            train_total += len(y_batch)

        # -- Validate --
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for x_batch, y_batch in val_loader:
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                logits = model(x_batch)
                loss = criterion(logits, y_batch)
                val_loss += loss.item() * len(y_batch)
                val_correct += (logits.argmax(1) == y_batch).sum().item()
                val_total += len(y_batch)

        train_loss /= train_total
        train_acc = train_correct / train_total
        val_loss /= val_total
        val_acc = val_correct / val_total
        lr = optimizer.param_groups[0]["lr"]
        scheduler.step()

        history["epoch"].append(epoch)
        history["train_loss"].append(round(train_loss, 5))
        history["train_acc"].append(round(train_acc, 4))
        history["val_loss"].append(round(val_loss, 5))
        history["val_acc"].append(round(val_acc, 4))
        history["lr"].append(round(lr, 8))

        marker = ""
        if val_acc > best_val_acc or (val_acc == best_val_acc and val_loss < best_val_loss):
            best_val_acc = val_acc
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), output_dir / "best.pt")
            marker = " *"
        else:
            patience_counter += 1

        if epoch <= 5 or epoch % 5 == 0 or epoch == EPOCHS or marker:
            print(f"{epoch:>6} {train_loss:>11.5f} {train_acc:>9.4f} {val_loss:>10.5f} {val_acc:>8.4f} {lr:>10.6f}{marker}")

        if patience_counter >= PATIENCE:
            print(f"\n  [STOP] Early stopping at epoch {epoch} (no improvement for {PATIENCE} epochs)")
            break

    # Save last checkpoint too
    torch.save(model.state_dict(), output_dir / "last.pt")

    # Save training history
    pd.DataFrame(history).to_csv(output_dir / "training_history.csv", index=False)

    return model, history


# ===================================================================
# EVALUATION & EXPORT
# ===================================================================

def evaluate_model(model, X_val, y_val, output_dir):
    """Full evaluation with classification report and confusion matrix."""
    device = next(model.parameters()).device
    model.eval()

    X_val_t = torch.tensor(X_val, dtype=torch.float32).permute(0, 2, 1).to(device)
    with torch.no_grad():
        logits = model(X_val_t)
        preds = logits.argmax(1).cpu().numpy()

    class_names = ["smooth_road", "pothole", "bump"]
    report = classification_report(y_val, preds, target_names=class_names, digits=4)
    cm = confusion_matrix(y_val, preds)

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(report)

    print("CONFUSION MATRIX")
    print("=" * 60)
    header = "".join(f"{name:>14}" for name in class_names)
    print(f"{'Predicted ->':>14}{header}")
    for i, name in enumerate(class_names):
        row = "".join(f"{cm[i, j]:>14}" for j in range(NUM_CLASSES))
        print(f"{'Actual ' + name:>14}{row}")
    print()

    # Save report
    with open(output_dir / "classification_report.txt", "w") as f:
        f.write("SETU 1D-CNN Sensor Model -- Evaluation Report\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(report + "\n\n")
        f.write("Confusion Matrix:\n")
        f.write(str(cm) + "\n")

    return report, cm


def export_model(model, output_dir):
    """Export to ONNX (and optionally INT8 quantised)."""
    device = next(model.parameters()).device
    model.eval()

    # -- Save full PyTorch model (state_dict already saved as best.pt) --
    torch.save(model, output_dir / "full_model.pt")

    # -- Export to ONNX --
    dummy_input = torch.randn(1, IN_CHANNELS, WINDOW_SIZE).to(device)
    onnx_path = output_dir / "pothole_sensor_model.onnx"
    torch.onnx.export(
        model,
        dummy_input,
        str(onnx_path),
        input_names=["imu_window"],
        output_names=["class_logits"],
        dynamic_axes={"imu_window": {0: "batch"}, "class_logits": {0: "batch"}},
        opset_version=13,
    )
    onnx_size_kb = onnx_path.stat().st_size / 1024
    print(f"  [OK] ONNX exported: {onnx_path.name} ({onnx_size_kb:.1f} KB)")

    # -- INT8 quantised PyTorch (CPU) --
    model_cpu = model.cpu()
    model_cpu.eval()
    quantised_model = torch.quantization.quantize_dynamic(
        model_cpu, {nn.Linear, nn.Conv1d}, dtype=torch.qint8
    )
    quantised_path = output_dir / "pothole_sensor_model_int8.pt"
    torch.save(quantised_model.state_dict(), quantised_path)
    quantised_size_kb = quantised_path.stat().st_size / 1024
    print(f"  [OK] INT8 quantised: {quantised_path.name} ({quantised_size_kb:.1f} KB)")

    # -- Save model config for reproducibility --
    config = {
        "model": "PotholeSensor1DCNN",
        "num_classes": NUM_CLASSES,
        "in_channels": IN_CHANNELS,
        "window_size": WINDOW_SIZE,
        "window_sec": WINDOW_SEC,
        "target_hz": TARGET_HZ,
        "overlap": OVERLAP,
        "bandpass": [BANDPASS_LOW, BANDPASS_HIGH],
        "class_map": {0: "smooth_road", 1: "pothole", 2: "bump"},
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "onnx_size_kb": round(onnx_size_kb, 1),
        "int8_size_kb": round(quantised_size_kb, 1),
        "exported_at": datetime.datetime.now().isoformat(),
    }
    with open(output_dir / "model_config.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"  [OK] Config saved: model_config.json")


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("=" * 62)
    print("  SETU -- 1D-CNN On-Device Sensor Model Training Pipeline")
    print("=" * 62)

    # Create unique output directory
    run_name = f"sensor_1dcnn_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = OUTPUT_BASE / run_name
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n  Output: {output_dir}")

    # -- Step 1: Load and preprocess data --
    print("\n" + "-" * 62)
    print("  STEP 1: Loading & Preprocessing Dataset")
    print("-" * 62)
    X, y = build_dataset()
    print(f"\n  Total windows extracted: {len(X)}")
    print(f"  Window shape: {X.shape[1:]} (timesteps={X.shape[1]}, channels={X.shape[2]})")
    for cls_id, cls_name in enumerate(["smooth_road", "pothole", "bump"]):
        count = (y == cls_id).sum()
        print(f"    Class {cls_id} ({cls_name}): {count} windows ({count/len(y)*100:.1f}%)")

    # -- Step 2: Train/Val split --
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n  Train: {len(X_train)} windows  |  Val: {len(X_val)} windows")

    # Save split info
    np.save(output_dir / "X_val.npy", X_val)
    np.save(output_dir / "y_val.npy", y_val)

    # -- Step 3: Train --
    print("\n" + "-" * 62)
    print("  STEP 2: Training 1D-CNN")
    print("-" * 62)
    model, history = train_model(X_train, y_train, X_val, y_val, output_dir)

    # Load best weights
    model.load_state_dict(torch.load(output_dir / "best.pt", weights_only=True))

    # -- Step 4: Evaluate --
    print("\n" + "-" * 62)
    print("  STEP 3: Evaluation (Best Checkpoint)")
    print("-" * 62)
    evaluate_model(model, X_val, y_val, output_dir)

    # -- Step 5: Export --
    print("-" * 62)
    print("  STEP 4: Exporting Models")
    print("-" * 62)
    export_model(model, output_dir)

    # -- Summary --
    best_epoch = np.argmax(history["val_acc"]) + 1
    best_acc = max(history["val_acc"])
    print("\n" + "=" * 62)
    print("  TRAINING COMPLETE")
    print("=" * 62)
    print(f"  Best validation accuracy: {best_acc:.4f} (epoch {best_epoch})")
    print(f"  All outputs saved to:")
    print(f"    {output_dir}")
    print(f"\n  Files:")
    for f in sorted(output_dir.iterdir()):
        size = f.stat().st_size
        if size > 1024 * 1024:
            print(f"    {f.name:<40} {size/1024/1024:.1f} MB")
        else:
            print(f"    {f.name:<40} {size/1024:.1f} KB")
    print("=" * 62)


if __name__ == "__main__":
    main()
