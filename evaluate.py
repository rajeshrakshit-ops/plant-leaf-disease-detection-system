"""
Plant Leaf Disease Detection - Model Evaluation & Performance Metrics
Computes Test Accuracy, Precision, Recall, F1-Score, and Per-Class Reports.
"""

import json
import argparse
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import classification_report, confusion_matrix

from train import build_model, NORM_MEAN, NORM_STD


@torch.no_grad()
def evaluate_model(checkpoint_path, test_dir, batch_size=32, img_size=224):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading checkpoint from: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    arch = checkpoint.get("arch", "mobilenet_v3")
    classes = checkpoint.get("classes")
    num_classes = len(classes)

    model = build_model(arch=arch, num_classes=num_classes, pretrained=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    test_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORM_MEAN, std=NORM_STD)
    ])

    test_dataset = datasets.ImageFolder(test_dir, transform=test_transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    print(f"Evaluating {len(test_dataset)} test samples across {num_classes} classes on {device}...")

    all_preds = []
    all_targets = []

    for images, targets in test_loader:
        images = images.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_targets.extend(targets.numpy())

    report = classification_report(all_targets, all_preds, target_names=classes, digits=4)
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(report)

    # Save metrics to json
    report_dict = classification_report(all_targets, all_preds, target_names=classes, output_dict=True)
    report_file = Path(checkpoint_path).parent / "evaluation_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2)
    print(f"Saved evaluation metrics to {report_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate trained plant disease model")
    parser.add_argument("--checkpoint", type=str, default="./models/best_model.pth", help="Path to checkpoint .pth")
    parser.add_argument("--test-dir", type=str, default="./data/PlantVillage/val", help="Path to test or val images")
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    evaluate_model(args.checkpoint, args.test_dir, args.batch_size)

