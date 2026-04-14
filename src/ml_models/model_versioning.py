import os
import json
import hashlib
import pandas as pd
from datetime import datetime
from pathlib import Path
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
VERSIONS_DIR = os.path.join(MODEL_DIR, "versions")


def compute_model_hash(model) -> str:
    model_bytes = joblib.dumps(model)
    hash_value = hashlib.sha256(model_bytes).hexdigest()
    return hash_value[:16]


def create_model_version(
    model_name: str,
    model,
    version: str = None,
    description: str = "",
    training_data_info: dict = None,
    metrics: dict = None,
    scaler=None,
) -> dict:
    if version is None:
        version = datetime.now().strftime("%Y%m%d_%H%M%S")

    model_hash = compute_model_hash(model)

    version_info = {
        "model_name": model_name,
        "version": version,
        "model_hash": model_hash,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "training_data_info": training_data_info or {},
        "metrics": metrics or {},
        "status": "active",
    }

    version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")
    os.makedirs(version_dir, exist_ok=True)

    model_path = os.path.join(version_dir, "model.joblib")
    joblib.dump(model, model_path)

    if scaler is not None:
        scaler_path = os.path.join(version_dir, "scaler.joblib")
        joblib.dump(scaler, scaler_path)

    version_info_path = os.path.join(version_dir, "version_info.json")
    with open(version_info_path, "w") as f:
        json.dump(version_info, f, indent=2)

    logger.info(f"Created version {version} for model {model_name}")

    return version_info


def list_versions(model_name: str = None) -> pd.DataFrame:
    versions = []

    if not os.path.exists(VERSIONS_DIR):
        return pd.DataFrame()

    for version_dir in os.listdir(VERSIONS_DIR):
        if model_name is None or version_dir.startswith(model_name):
            version_path = os.path.join(VERSIONS_DIR, version_dir)
            version_info_path = os.path.join(version_path, "version_info.json")

            if os.path.exists(version_info_path):
                with open(version_info_path, "r") as f:
                    version_info = json.load(f)
                versions.append(version_info)

    return pd.DataFrame(versions)


def get_version_info(model_name: str, version: str) -> dict:
    version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")
    version_info_path = os.path.join(version_dir, "version_info.json")

    if not os.path.exists(version_info_path):
        raise ValueError(f"Version {version} not found for model {model_name}")

    with open(version_info_path, "r") as f:
        version_info = json.load(f)

    return version_info


def load_version(model_name: str, version: str = None) -> tuple:
    if version is None:
        versions_df = list_versions(model_name)
        if versions_df.empty:
            raise ValueError(f"No versions found for model {model_name}")
        version = versions_df.iloc[0]["version"]

    version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")
    model_path = os.path.join(version_dir, "model.joblib")

    if not os.path.exists(model_path):
        raise ValueError(f"Model file not found for {model_name} version {version}")

    model = joblib.load(model_path)

    scaler = None
    scaler_path = os.path.join(version_dir, "scaler.joblib")
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)

    return model, scaler


def archive_version(model_name: str, version: str) -> dict:
    version_dir = os.path.join(VERSIONS_DIR, f"{model_name}_{version}")
    version_info_path = os.path.join(version_dir, "version_info.json")

    with open(version_info_path, "r") as f:
        version_info = json.load(f)

    version_info["status"] = "archived"
    version_info["archived_at"] = datetime.now().isoformat()

    with open(version_info_path, "w") as f:
        json.dump(version_info, f, indent=2)

    logger.info(f"Archived version {version} of {model_name}")

    return version_info


def compare_versions(model_name: str, version1: str, version2: str) -> dict:
    info1 = get_version_info(model_name, version1)
    info2 = get_version_info(model_name, version2)

    return {
        "version1": version1,
        "version2": version2,
        "metrics_comparison": {
            version1: info1.get("metrics", {}),
            version2: info2.get("metrics", {}),
        },
        "training_data_comparison": {
            version1: info1.get("training_data_info", {}),
            version2: info2.get("training_data_info", {}),
        },
    }
