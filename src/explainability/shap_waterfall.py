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
WATERFALL_DIR = os.path.join(MODEL_DIR, "waterfall_plots")
os.makedirs(WATERFALL_DIR, exist_ok=True)


def create_shap_waterfall_plot(
    explainer,
    shap_values: np.ndarray,
    X: pd.DataFrame,
    sample_index: int = 0,
    save_path: str = None,
):
    X = X.fillna(0)

    if save_path is None:
        save_path = os.path.join(WATERFALL_DIR, f"waterfall_{sample_index}.png")

    expected_value = explainer.expected_value
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = (
            expected_value[1] if len(expected_value) > 1 else expected_value[0]
        )

    explanation = shap.Explanation(
        values=shap_values[sample_index, :],
        base_values=expected_value,
        data=X.iloc[sample_index, :],
        feature_names=X.columns.tolist(),
    )

    plt.figure(figsize=(10, 8))
    shap.plots.waterfall(explanation, show=False)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"Waterfall plot saved to {save_path}")
    return save_path


def create_batch_waterfall_plots(
    explainer,
    shap_values: np.ndarray,
    X: pd.DataFrame,
    n_samples: int = 10,
    save_dir: str = None,
):
    X = X.fillna(0)

    if save_dir is None:
        save_dir = WATERFALL_DIR

    os.makedirs(save_dir, exist_ok=True)

    expected_value = explainer.expected_value
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = (
            expected_value[1] if len(expected_value) > 1 else expected_value[0]
        )

    saved_plots = []
    for i in range(min(n_samples, len(X))):
        save_path = os.path.join(save_dir, f"waterfall_{i}.png")

        explanation = shap.Explanation(
            values=shap_values[i, :],
            base_values=expected_value,
            data=X.iloc[i, :],
            feature_names=X.columns.tolist(),
        )

        plt.figure(figsize=(10, 8))
        shap.plots.waterfall(explanation, show=False)
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        saved_plots.append(save_path)

    logger.info(f"Created {len(saved_plots)} waterfall plots")
    return saved_plots
