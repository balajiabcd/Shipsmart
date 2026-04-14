import os
import joblib
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
VERSIONS_DIR = os.path.join(MODEL_DIR, "versions")
os.makedirs(VERSIONS_DIR, exist_ok=True)


def save_model(
    model, model_name: str, version: str = None, metadata: dict = None, scaler=None
) -> str:
    if version is None:
        version = datetime.now().strftime("%Y%m%d_%H%M%S")

    version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")
    os.makedirs(version_dir, exist_ok=True)

    model_path = os.path.join(version_dir, "model.joblib")
    joblib.dump(model, model_path)

    if scaler is not None:
        scaler_path = os.path.join(version_dir, "scaler.joblib")
        joblib.dump(scaler, scaler_path)

    if metadata is None:
        metadata = {}
    metadata["model_name"] = model_name
    metadata["version"] = version
    metadata["created_at"] = datetime.now().isoformat()

    metadata_path = os.path.join(version_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Model saved: {model_name} version {version}")

    return version_dir


def load_model(model_name: str, version: str = None) -> tuple:
    if version is None:
        version_dirs = [d for d in os.listdir(VERSIONS_DIR) if d.startswith(model_name)]
        if not version_dirs:
            raise ValueError(f"No versions found for model {model_name}")
        version_dirs.sort(reverse=True)
        latest_version = version_dirs[0].replace(f"{model_name}_", "")
        version_dir = os.path.join(VERSIONS_DIR, version_dirs[0])
    else:
        version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")

    model_path = os.path.join(version_dir, "model.joblib")
    model = joblib.load(model_path)

    scaler = None
    scaler_path = os.path.join(version_dir, "scaler.joblib")
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)

    metadata_path = os.path.join(version_dir, "metadata.json")
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    logger.info(f"Model loaded: {model_name} version {version}")

    return model, scaler, metadata


def list_model_versions(model_name: str = None) -> pd.DataFrame:
    versions = []

    for version_dir in os.listdir(VERSIONS_DIR):
        if model_name is None or version_dir.startswith(model_name):
            version_path = os.path.join(VERSIONS_DIR, version_dir)
            metadata_path = os.path.join(version_path, "metadata.json")

            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                versions.append(metadata)
            else:
                versions.append(
                    {
                        "model_name": version_dir,
                        "version": version_dir,
                        "created_at": "Unknown",
                    }
                )

    return pd.DataFrame(versions)


def delete_model_version(model_name: str, version: str) -> bool:
    version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")

    if os.path.exists(version_dir):
        shutil.rmtree(version_dir)
        logger.info(f"Deleted model {model_name} version {version}")
        return True

    return False


def export_model(
    model, export_path: str, model_name: str, metadata: dict = None
) -> str:
    os.makedirs(os.path.dirname(export_path), exist_ok=True)

    joblib.dump(model, export_path)

    if metadata is not None:
        metadata_path = export_path.replace(".joblib", "_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

    logger.info(f"Model exported to {export_path}")

    return export_path


def import_model(import_path: str) -> tuple:
    model = joblib.load(import_path)

    metadata = {}
    metadata_path = import_path.replace(".joblib", "_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    return model, metadata
