"""
Plant Leaf Disease Detection System - High-Performance FastAPI Backend
Serves REST API endpoints for leaf disease diagnosis, disease knowledge base,
and hosts the responsive web frontend.
"""

import os
import io
import time
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image

try:
    import torch
    import torch.nn as nn
    from torchvision import transforms, models
    TORCH_AVAILABLE = True
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inference_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
except ImportError:
    TORCH_AVAILABLE = False
    DEVICE = "cpu"
    torch = None
    nn = None
    transforms = None
    models = None
    inference_transform = None

from backend.disease_knowledge import DISEASE_DATABASE

app = FastAPI(
    title="PlantGuard AI - Plant Leaf Disease Detection API",
    description="Deep learning powered plant leaf pathology diagnosis and treatment advisory.",
    version="2.0.0"
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path definitions
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pth"
FRONTEND_DIR = BASE_DIR / "frontend"

# Global model state
loaded_model: Optional[Any] = None
model_classes: List[str] = []
is_demo_mode: bool = True


def load_pytorch_model():
    """Attempts to load trained PyTorch checkpoint or sets demo mode."""
    global loaded_model, model_classes, is_demo_mode

    if not TORCH_AVAILABLE:
        print("[i] PyTorch not installed in this environment. Running in Demo / Simulation Mode.")
        is_demo_mode = True
        return

    if MODEL_PATH.exists():
        try:
            print(f"[*] Found trained checkpoint at: {MODEL_PATH}")
            checkpoint = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)
            arch = checkpoint.get("arch", "mobilenet_v3")
            model_classes = checkpoint.get("classes", [])
            num_classes = len(model_classes) if model_classes else 38

            # Rebuild architecture
            if arch == "mobilenet_v3":
                model = models.mobilenet_v3_large(weights=None)
                in_features = model.classifier[0].in_features
                model.classifier = nn.Sequential(
                    nn.Linear(in_features, 512),
                    nn.Hardswish(),
                    nn.Dropout(p=0.3),
                    nn.Linear(512, num_classes)
                )
            elif arch == "resnet50":
                model = models.resnet50(weights=None)
                in_features = model.fc.in_features
                model.fc = nn.Sequential(
                    nn.Linear(in_features, 512),
                    nn.ReLU(inplace=True),
                    nn.Dropout(p=0.3),
                    nn.Linear(512, num_classes)
                )
            elif arch == "efficientnet_b0":
                model = models.efficientnet_b0(weights=None)
                in_features = model.classifier[1].in_features
                model.classifier = nn.Sequential(
                    nn.Dropout(p=0.3),
                    nn.Linear(in_features, 512),
                    nn.SiLU(),
                    nn.Dropout(p=0.2),
                    nn.Linear(512, num_classes)
                )
            else:
                raise ValueError(f"Unknown architecture: {arch}")

            model.load_state_dict(checkpoint["model_state_dict"])
            model.to(DEVICE)
            model.eval()

            loaded_model = model
            is_demo_mode = False
            print(f"[✓] Successfully loaded {arch} with {num_classes} classes on {DEVICE}.")
            return
        except Exception as e:
            print(f"[!] Warning: Failed to load checkpoint ({e}). Falling back to simulation mode.")

    print("[i] Model checkpoint not found yet. Running in Demo / Simulation Mode.")
    print("    Train a real model anytime with: python train.py")
    is_demo_mode = True


# Run model loader on startup
load_pytorch_model()


@app.get("/api/health")
def health_check():
    """Service health and runtime telemetry."""
    return {
        "status": "online",
        "torch_available": TORCH_AVAILABLE,
        "device": str(DEVICE),
        "cuda_available": torch.cuda.is_available() if TORCH_AVAILABLE and torch else False,
        "model_loaded": not is_demo_mode,
        "mode": "production_pytorch" if not is_demo_mode else "demo_simulation",
        "supported_classes": len(DISEASE_DATABASE)
    }


@app.get("/api/diseases")
def get_all_diseases(search: Optional[str] = None, plant: Optional[str] = None, category: Optional[str] = None):
    """
    Returns disease encyclopedia catalog with optional filtering.
    """
    results = list(DISEASE_DATABASE.values())

    if plant:
        results = [d for d in results if d["plant"].lower() == plant.lower()]
    if category:
        results = [d for d in results if d["category"].lower() == category.lower()]
    if search:
        q = search.lower()
        results = [
            d for d in results
            if q in d["plant"].lower() or q in d["condition"].lower() or q in d["visual_symptoms"].lower()
        ]

    plants = sorted(list(set(d["plant"] for d in DISEASE_DATABASE.values())))
    categories = sorted(list(set(d["category"] for d in DISEASE_DATABASE.values())))

    return {
        "total": len(results),
        "available_plants": plants,
        "available_categories": categories,
        "diseases": results
    }


@app.get("/api/disease/{disease_id}")
def get_disease_detail(disease_id: int):
    """Retrieve full clinical guide for a specific disease class index."""
    if disease_id not in DISEASE_DATABASE:
        raise HTTPException(status_code=404, detail="Disease ID not found in database.")
    return DISEASE_DATABASE[disease_id]


@app.post("/api/predict")
async def predict_leaf_disease(file: UploadFile = File(...)):
    """
    Receives leaf image, runs deep learning inference, maps to disease database,
    and returns rich diagnosis and treatment recommendations.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image (JPEG/PNG/WEBP).")

    start_time = time.time()

    # Read and parse image
    try:
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    # Preprocessing
    tensor_img = None
    if TORCH_AVAILABLE and inference_transform is not None:
        tensor_img = inference_transform(pil_img).unsqueeze(0).to(DEVICE)

    top_predictions = []
    best_index = 0
    confidence = 0.0

    if not is_demo_mode and loaded_model is not None and tensor_img is not None:
        # Real Deep Learning Forward Pass
        with torch.no_grad():
            logits = loaded_model(tensor_img)
            probs = torch.softmax(logits, dim=1)[0]
            top_k_probs, top_k_indices = torch.topk(probs, k=min(3, len(probs)))

            best_index = int(top_k_indices[0].item())
            confidence = float(top_k_probs[0].item()) * 100

            for prob, idx in zip(top_k_probs, top_k_indices):
                cls_idx = int(idx.item())
                entry = DISEASE_DATABASE.get(cls_idx, {})
                top_predictions.append({
                    "class_index": cls_idx,
                    "condition": entry.get("condition", f"Class {cls_idx}"),
                    "plant": entry.get("plant", "Unknown"),
                    "confidence": round(float(prob.item()) * 100, 2)
                })
    else:
        # Intelligent fallback / Demo simulation mode
        # Deterministically hashes file size & dimensions for consistent demo response
        seed_val = (len(contents) + pil_img.width + pil_img.height) % len(DISEASE_DATABASE)
        # Select one realistic disease or healthy
        demo_candidates = [29, 20, 0, 7, 30, 25, 37, 3, 10, 18] # Early blight, scab, healthy, etc.
        best_index = demo_candidates[seed_val % len(demo_candidates)]
        confidence = 96.85

        top_predictions = [
            {
                "class_index": best_index,
                "condition": DISEASE_DATABASE[best_index]["condition"],
                "plant": DISEASE_DATABASE[best_index]["plant"],
                "confidence": confidence
            },
            {
                "class_index": (best_index + 1) % len(DISEASE_DATABASE),
                "condition": DISEASE_DATABASE[(best_index + 1) % len(DISEASE_DATABASE)]["condition"],
                "plant": DISEASE_DATABASE[(best_index + 1) % len(DISEASE_DATABASE)]["plant"],
                "confidence": 2.15
            },
            {
                "class_index": (best_index + 2) % len(DISEASE_DATABASE),
                "condition": DISEASE_DATABASE[(best_index + 2) % len(DISEASE_DATABASE)]["condition"],
                "plant": DISEASE_DATABASE[(best_index + 2) % len(DISEASE_DATABASE)]["plant"],
                "confidence": 1.00
            }
        ]

    disease_info = DISEASE_DATABASE.get(best_index, {
        "class_name": f"Class_{best_index}",
        "plant": "Unknown",
        "condition": "Detected Condition",
        "category": "Unknown",
        "is_healthy": False,
        "pathogen": "N/A",
        "severity": "Unknown",
        "visual_symptoms": "Please consult local agricultural extension officer.",
        "organic_treatment": [],
        "chemical_treatment": [],
        "prevention": []
    })

    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "status": "success",
        "engine": "PyTorch Neural Network" if not is_demo_mode else "Demo Simulation Mode (Train model via train.py)",
        "inference_time_ms": elapsed_ms,
        "is_demo_mode": is_demo_mode,
        "diagnosis": {
            "class_index": best_index,
            "plant": disease_info["plant"],
            "condition": disease_info["condition"],
            "category": disease_info["category"],
            "is_healthy": disease_info["is_healthy"],
            "severity": disease_info["severity"],
            "confidence": round(confidence, 2),
            "pathogen": disease_info.get("pathogen", "N/A"),
            "visual_symptoms": disease_info["visual_symptoms"],
            "organic_treatment": disease_info["organic_treatment"],
            "chemical_treatment": disease_info["chemical_treatment"],
            "prevention": disease_info["prevention"]
        },
        "top_candidates": top_predictions
    }


# Mount and serve Frontend static files
if FRONTEND_DIR.exists():
    # Mount /static for backward compatibility
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    # Mount root with html=True so index.html, styles.css, app.js are served at root
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    @app.get("/")
    def serve_root_api():
        return {
            "status": "online",
            "service": "PlantGuard AI Backend API",
            "docs": "/docs",
            "health": "/api/health"
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=False)

