import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
PDP_DIR = os.path.join(MODEL_DIR, "pdp")
os.makedirs(PDP_DIR, exist_ok=True)


def create_partial_dependence_plot(
    model,
    X: pd.DataFrame,
    features: list,
    save_path: str = None,
    kind: str = "both",
    subsample: int = 1000,
):
    if isinstance(features[0], str):
        feature_indices = [list(X.columns).index(f) for f in features]
    else:
        feature_indices = features

    if save_path is None:
        save_path = os.path.join(PDP_DIR, "partial_dependence_grid.png")

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    display = PartialDependenceDisplay.from_estimator(
        model,
        X,
        feature_indices[:8],
        ax=axes,
        n_jobs=-1,
        kind=kind,
        subsample=subsample,
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"Partial dependence plot saved to {save_path}")
    return save_path


def create_individual_pdp(
    model,
    X: pd.DataFrame,
    feature_name: str,
    save_path: str = None,
    kind: str = "both",
    subsample: int = 1000,
):
    feature_idx = list(X.columns).index(feature_name)

    if save_path is None:
        save_path = os.path.join(PDP_DIR, f"{feature_name}_pdp.png")

    plt.figure(figsize=(10, 6))
    PartialDependenceDisplay.from_estimator(
        model, X, [feature_idx], kind=kind, subsample=subsample
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"Partial dependence plot for {feature_name} saved to {save_path}")
    return save_path


def create_batch_pdp(
    model,
    X: pd.DataFrame,
    feature_names: list,
    save_dir: str = None,
    kind: str = "both",
    subsample: int = 1000,
):
    if save_dir is None:
        save_dir = PDP_DIR

    os.makedirs(save_dir, exist_ok=True)

    saved_plots = []
    for feature in feature_names:
        save_path = os.path.join(save_dir, f"{feature}_pdp.png")
        create_individual_pdp(model, X, feature, save_path, kind, subsample)
        saved_plots.append(save_path)

    logger.info(f"Created {len(saved_plots)} partial dependence plots")
    return saved_plots


def create_ice_plots(
    model,
    X: pd.DataFrame,
    feature_name: str,
    save_path: str = None,
    n_samples: int = 100,
):
    feature_idx = list(X.columns).index(feature_name)

    if save_path is None:
        save_path = os.path.join(PDP_DIR, f"{feature_name}_ice.png")

    plt.figure(figsize=(10, 6))
    PartialDependenceDisplay.from_estimator(
        model, X, [feature_idx], kind="both", subsample=n_samples, ice_lines=True
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"ICE plot for {feature_name} saved to {save_path}")
    return save_path


def create_2d_interaction_plot(
    model, X: pd.DataFrame, feature1: str, feature2: str, save_path: str = None
):
    features = [feature1, feature2]
    feature_indices = [list(X.columns).index(f) for f in features]

    if save_path is None:
        save_path = os.path.join(PDP_DIR, f"{feature1}_x_{feature2}_pdp.png")

    plt.figure(figsize=(10, 8))
    PartialDependenceDisplay.from_estimator(model, X, [feature_indices], kind="average")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"2D interaction plot saved to {save_path}")
    return save_path
