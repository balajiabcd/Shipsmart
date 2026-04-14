import os
import numpy as np
import pandas as pd
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


def calculate_permutation_importance(
    model,
    X: pd.DataFrame,
    y: pd.Series,
    n_repeats: int = 10,
    test_size: float = 0.2,
    random_state: int = 42,
    n_jobs: int = -1,
):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    logger.info("Calculating permutation importance...")
    result = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=n_jobs,
    )

    importance_df = pd.DataFrame(
        {
            "feature": X.columns,
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
            "importance_max": result.importances_max,
        }
    ).sort_values("importance_mean", ascending=False)

    logger.info("Permutation importance calculated")
    return importance_df, result


def save_permutation_importance(importance_df: pd.DataFrame, filepath: str = None):
    if filepath is None:
        filepath = os.path.join(MODEL_DIR, "permutation_importance.csv")

    importance_df.to_csv(filepath, index=False)
    logger.info(f"Permutation importance saved to {filepath}")
    return filepath


def load_permutation_importance(filepath: str = None) -> pd.DataFrame:
    if filepath is None:
        filepath = os.path.join(MODEL_DIR, "permutation_importance.csv")

    importance_df = pd.read_csv(filepath)
    logger.info(f"Loaded permutation importance from {filepath}")
    return importance_df


def plot_permutation_importance(
    importance_df: pd.DataFrame, save_path: str = None, top_n: int = 20
):
    importance_df = importance_df.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))

    y_pos = np.arange(len(importance_df))
    ax.barh(
        y_pos,
        importance_df["importance_mean"],
        xerr=importance_df["importance_std"],
        align="center",
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(importance_df["feature"])
    ax.invert_yaxis()
    ax.set_xlabel("Permutation Importance")
    ax.set_title(f"Top {top_n} Features by Permutation Importance")

    plt.tight_layout()

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "permutation_importance.png")

    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"Permutation importance plot saved to {save_path}")
    return save_path


def compare_permutation_shap(
    permutation_df: pd.DataFrame, shap_df: pd.DataFrame
) -> pd.DataFrame:
    comparison = pd.merge(
        permutation_df.rename(columns={"importance_mean": "permutation_importance"}),
        shap_df.rename(columns={"importance": "shap_importance"}),
        on="feature",
        how="outer",
    ).fillna(0)

    comparison["permutation_rank"] = (
        comparison["permutation_importance"].rank(ascending=False).astype(int)
    )
    comparison["shap_rank"] = (
        comparison["shap_importance"].rank(ascending=False).astype(int)
    )
    comparison["rank_difference"] = abs(
        comparison["permutation_rank"] - comparison["shap_rank"]
    )

    comparison = comparison.sort_values("shap_importance", ascending=False)

    return comparison
