import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


def create_shap_dependence_plot(
    shap_values: np.ndarray,
    X: pd.DataFrame,
    feature_name: str,
    save_path: str = None,
    interaction_index: str = "auto",
    show: bool = False,
):
    X = X.fillna(0)

    if feature_name not in X.columns:
        logger.warning(f"Feature {feature_name} not found in X.columns")
        return None

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, f"shap_dependence_{feature_name}.png")

    plt.figure(figsize=(8, 6))
    shap.dependence_plot(
        feature_name, shap_values, X, interaction_index=interaction_index, show=show
    )
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"SHAP dependence plot saved to {save_path}")
    return save_path


def create_all_dependence_plots(
    shap_values: np.ndarray, X: pd.DataFrame, top_n: int = 5, save_dir: str = None
):
    X = X.fillna(0)

    if save_dir is None:
        save_dir = MODEL_DIR

    feature_importance = np.abs(shap_values).mean(axis=0)
    top_indices = np.argsort(feature_importance)[-top_n:]
    top_features = X.columns[top_indices]

    saved_plots = []
    for feature in top_features:
        save_path = os.path.join(save_dir, f"shap_dependence_{feature}.png")
        create_shap_dependence_plot(shap_values, X, feature, save_path)
        saved_plots.append(save_path)

    logger.info(f"Created {len(saved_plots)} dependence plots for top {top_n} features")
    return saved_plots


def get_top_features(
    shap_values: np.ndarray, feature_names: list, top_n: int = 10
) -> list:
    importance = np.abs(shap_values).mean(axis=0)
    top_indices = np.argsort(importance)[-top_n:][::-1]
    return [feature_names[i] for i in top_indices]
