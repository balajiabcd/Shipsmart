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
FORCE_PLOTS_DIR = os.path.join(MODEL_DIR, "force_plots")
os.makedirs(FORCE_PLOTS_DIR, exist_ok=True)


def create_shap_force_plot(
    explainer,
    shap_values: np.ndarray,
    X: pd.DataFrame,
    sample_index: int = 0,
    save_path: str = None,
):
    X = X.fillna(0)

    if save_path is None:
        save_path = os.path.join(FORCE_PLOTS_DIR, f"force_{sample_index}.png")

    expected_value = explainer.expected_value
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = (
            expected_value[1] if len(expected_value) > 1 else expected_value[0]
        )

    plt.figure(figsize=(20, 4))
    shap.force_plot(
        expected_value,
        shap_values[sample_index, :],
        X.iloc[sample_index, :],
        matplotlib=True,
        show=False,
    )
    plt.savefig(save_path, dpi=100, bbox_inches="tight")
    plt.close()

    logger.info(f"Force plot saved to {save_path}")
    return save_path


def create_force_plot_html(
    shap_values: np.ndarray, X: pd.DataFrame, save_path: str = None
):
    X = X.fillna(0)

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "shap_force_plot.html")

    shap.initjs()
    expected_value = (
        shap_values.mean(axis=0) if len(shap_values.shape) > 1 else shap_values.mean()
    )

    html = shap.force_plot(expected_value, shap_values[:100], X.iloc[:100], show=False)

    with open(save_path, "w") as f:
        f.write(html.html())

    logger.info(f"Interactive force plot HTML saved to {save_path}")
    return save_path


def create_batch_force_plots(
    explainer,
    shap_values: np.ndarray,
    X: pd.DataFrame,
    n_samples: int = 10,
    save_dir: str = None,
):
    X = X.fillna(0)

    if save_dir is None:
        save_dir = FORCE_PLOTS_DIR

    os.makedirs(save_dir, exist_ok=True)

    expected_value = explainer.expected_value
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = (
            expected_value[1] if len(expected_value) > 1 else expected_value[0]
        )

    saved_plots = []
    for i in range(min(n_samples, len(X))):
        save_path = os.path.join(save_dir, f"force_{i}.png")
        plt.figure(figsize=(20, 4))
        shap.force_plot(
            expected_value, shap_values[i, :], X.iloc[i, :], matplotlib=True, show=False
        )
        plt.savefig(save_path, dpi=100, bbox_inches="tight")
        plt.close()
        saved_plots.append(save_path)

    logger.info(f"Created {len(saved_plots)} force plots")
    return saved_plots
