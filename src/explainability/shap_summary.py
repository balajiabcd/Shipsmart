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
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "images")
os.makedirs(DOCS_DIR, exist_ok=True)


def create_shap_summary_plot(
    shap_values: np.ndarray = None,
    X: pd.DataFrame = None,
    save_path: str = None,
    show: bool = False,
    plot_type: str = "dot",
):
    if shap_values is None:
        shap_values = np.load(os.path.join(MODEL_DIR, "shap_values.npy"))
        logger.info("Loaded SHAP values from file")

    if X is None:
        raise ValueError("Feature data (X) is required")

    X = X.fillna(0)

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "shap_summary.png")

    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X, show=show, plot_type=plot_type)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"SHAP summary plot saved to {save_path}")
    return save_path


def create_shap_summary_bar_plot(
    shap_values: np.ndarray = None, X: pd.DataFrame = None, save_path: str = None
):
    if shap_values is None:
        shap_values = np.load(os.path.join(MODEL_DIR, "shap_values.npy"))

    if X is None:
        raise ValueError("Feature data (X) is required")

    X = X.fillna(0)

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "shap_summary_bar.png")

    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"SHAP summary bar plot saved to {save_path}")
    return save_path


def get_feature_importance_from_shap(
    shap_values: np.ndarray, feature_names: list = None
) -> pd.DataFrame:
    importance = np.abs(shap_values).mean(axis=0)

    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(len(importance))]

    importance_df = pd.DataFrame(
        {"feature": feature_names, "importance": importance}
    ).sort_values("importance", ascending=False)

    return importance_df
