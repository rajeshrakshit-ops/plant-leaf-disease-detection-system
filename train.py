"""
Plant Leaf Disease Detection - Deep Learning Model Training Pipeline
Framework: PyTorch & Torchvision
Supported Architectures: MobileNetV3-Large (Default), EfficientNet-B0, ResNet50
Dataset: PlantVillage (38 Classes)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms, models

# Ensure output models directory exists
MODEL_DIR = Path("./models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Standard ImageNet normalization parameters
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]


def get_data_transforms(img_size=224):
    """Data augmentation for training and clean transform for validation."""
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(degrees=25),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORM_MEAN, std=NORM_STD)
    ])

    val_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORM_MEAN, std=NORM_STD)
    ])

    return train_transform, val_transform


def build_model(arch="mobilenet_v3", num_classes=38, pretrained=True):
    """
    Builds transfer learning model backbone with customized classifier head.
    """
    print(f"Building {arch} model (pretrained={pretrained}, num_classes={num_classes})...")

    if arch == "mobilenet_v3":
        weights = models.MobileNet_V3_Large_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_large(weights=weights)
        in_features = model.classifier[0].in_features
        model.classifier = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.Hardswish(),
            nn.Dropout(p=0.3),
            nn.Linear(512, num_classes)
        )
    elif arch == "resnet50":
        weights = models.ResNet50_Weights.DEFAULT if pretrained else None
        model = models.resnet50(weights=weights)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(512, num_classes)
        )
    elif arch == "efficientnet_b0":
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = models.efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 512),
            nn.SiLU(),
            nn.Dropout(p=0.2),
            nn.Linear(512, num_classes)
        )
    else:
        raise ValueError(f"Unsupported architecture: {arch}")

    return model


def prepare_datasets(data_dir, img_size=224, val_split=0.2, batch_size=32, num_workers=2):
    """
    Detects dataset layout:
    - If data_dir has 'train' and 'val' subfolders, load them directly.
    - If data_dir has class subfolders directly, split into 80% train / 20% val.
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset directory '{data_dir}' not found!\n"
            f"Please download the PlantVillage dataset to '{data_dir}' or specify --data-dir.\n"
            f"See README.md for download instructions."
        )

    train_transform, val_transform = get_data_transforms(img_size)

    # Check for train/val split folders
    train_dir = data_path / "train"
    val_dir = data_path / "val"
    if not val_dir.exists():
        val_dir = data_path / "valid"

    if train_dir.exists() and val_dir.exists():
        print(f"Loading separate train and val directories from {data_path}...")
        train_dataset = datasets.ImageFolder(str(train_dir), transform=train_transform)
        val_dataset = datasets.ImageFolder(str(val_dir), transform=val_transform)
        class_names = train_dataset.classes
    else:
        print(f"Loading dataset from {data_path} and splitting {100*(1-val_split):.0f}% train / {100*val_split:.0f}% val...")
        full_dataset = datasets.ImageFolder(str(data_path))
        class_names = full_dataset.classes

        val_size = int(len(full_dataset) * val_split)
        train_size = len(full_dataset) - val_size

        # Deterministic split
        generator = torch.Generator().manual_seed(42)
        train_subset, val_subset = random_split(full_dataset, [train_size, val_size], generator=generator)

        # Apply respective transforms
        class DatasetWithTransform(torch.utils.data.Dataset):
            def __init__(self, subset, transform):
                self.subset = subset
                self.transform = transform

            def __getitem__(self, idx):
                img, label = self.subset[idx]
                return self.transform(img), label

            def __len__(self):
                return len(self.subset)

        train_dataset = DatasetWithTransform(train_subset, train_transform)
        val_dataset = DatasetWithTransform(val_subset, val_transform)

    print(f"Dataset stats: {len(train_dataset)} training images, {len(val_dataset)} validation images.")
    print(f"Detected {len(class_names)} classes.")

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )

    return train_loader, val_loader, class_names


def train_one_epoch(model, dataloader, criterion, optimizer, scaler, device):
    """Executes single training epoch with mixed precision."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad()

        # Automatic Mixed Precision for fast GPU throughput
        if device.type == "cuda":
            with torch.amp.autocast('cuda'):
                outputs = model(images)
                loss = criterion(outputs, labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


@torch.no_grad()
def evaluate_epoch(model, dataloader, criterion, device):
    """Evaluates validation loss and top-1 accuracy."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        outputs = model(images)
        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def export_onnx(model, save_path, img_size=224):
    """Exports trained PyTorch model to ONNX for cross-platform fast deployment."""
    try:
        model.eval()
        dummy_input = torch.randn(1, 3, img_size, img_size, device="cpu")
        cpu_model = model.to("cpu")
        torch.onnx.export(
            cpu_model,
            dummy_input,
            save_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
        )
        print(f"Exported ONNX model successfully to {save_path}")
    except Exception as e:
        print(f"ONNX export warning: {e}")


def main():
    parser = argparse.ArgumentParser(description="Train Plant Leaf Disease Detection Model")
    parser.add_argument("--data-dir", type=str, default="./data/PlantVillage", help="Path to PlantVillage dataset folder")
    parser.add_argument("--arch", type=str, default="mobilenet_v3", choices=["mobilenet_v3", "resnet50", "efficientnet_b0"], help="Backbone model")
    parser.add_argument("--epochs", type=int, default=15, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--lr", type=float, default=1e-3, help="Initial learning rate")
    parser.add_argument("--img-size", type=int, default=224, help="Input image dimension (224)")
    parser.add_argument("--workers", type=int, default=2, help="DataLoader worker processes")
    args = parser.parse_args()

    # Determine compute device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 60)
    print(f"PlantGuard Deep Learning Training Engine")
    print(f"Device: {device} | CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU Model: {torch.cuda.get_device_name(0)}")
    print(f"Model Backbone: {args.arch} | Image Resolution: {args.img_size}x{args.img_size}")
    print("=" * 60)

    # 1. Prepare Data
    train_loader, val_loader, class_names = prepare_datasets(
        data_dir=args.data_dir,
        img_size=args.img_size,
        batch_size=args.batch_size,
        num_workers=args.workers
    )

    num_classes = len(class_names)

    # Save class mapping JSON
    class_map_file = MODEL_DIR / "class_indices.json"
    with open(class_map_file, "w", encoding="utf-8") as f:
        json.dump({i: name for i, name in enumerate(class_names)}, f, indent=2)
    print(f"Saved class index mapping to {class_map_file}")

    # 2. Build Model
    model = build_model(arch=args.arch, num_classes=num_classes, pretrained=True)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)
    scaler = torch.amp.GradScaler('cuda', enabled=(device.type == "cuda"))

    # 3. Training Loop
    best_val_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    best_model_path = MODEL_DIR / "best_model.pth"

    start_training_time = time.time()

    for epoch in range(1, args.epochs + 1):
        epoch_start = time.time()

        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, scaler, device)
        val_loss, val_acc = evaluate_epoch(model, val_loader, criterion, device)
        scheduler.step()

        elapsed = time.time() - epoch_start

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        print(
            f"Epoch [{epoch:02d}/{args.epochs:02d}] "
            f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.2f}% | "
            f"Time: {elapsed:.1f}s"
        )

        # Checkpoint if validation accuracy improved
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'arch': args.arch,
                'num_classes': num_classes,
                'model_state_dict': model.state_dict(),
                'best_val_acc': best_val_acc,
                'classes': class_names
            }, best_model_path)
            print(f"  --> Saved new best checkpoint (Val Acc: {best_val_acc*100:.2f}%) to {best_model_path}")

    total_time = (time.time() - start_training_time) / 60
    print("=" * 60)
    print(f"Training Complete! Total time: {total_time:.2f} minutes")
    print(f"Highest Validation Accuracy: {best_val_acc*100:.2f}%")
    print(f"Best Weights Stored at: {best_model_path}")

    # Save training history
    history_path = MODEL_DIR / "training_history.json"
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
    print(f"Saved training history to {history_path}")

    # Export ONNX model for high performance inference
    onnx_path = MODEL_DIR / "plant_disease_model.onnx"
    export_onnx(model, onnx_path, img_size=args.img_size)
    print("=" * 60)


if __name__ == "__main__":
    main()

