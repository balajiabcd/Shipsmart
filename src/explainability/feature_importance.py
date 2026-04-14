import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


def generate_shap_feature_importance(
    shap_values: np.ndarray, feature_names: list = None
) -> pd.DataFrame:
    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(shap_values.shape[1])]

    importance = np.abs(shap_values).mean(axis=0)

    feature_importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importance,
            "std": np.abs(shap_values).std(axis=0),
        }
    ).sort_values("importance", ascending=False)

    return feature_importance


def generate_model_feature_importance(
    model, feature_names: list = None
) -> pd.DataFrame:
    if not hasattr(model, "feature_importances_"):
        logger.warning("Model does not have feature_importances_ attribute")
        return None

    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(len(model.feature_importances_))]

    importance = model.feature_importances_

    feature_importance = pd.DataFrame(
        {"feature": feature_names, "importance": importance}
    ).sort_values("importance", ascending=False)

    return feature_importance


def compare_feature_importance(
    shap_values: np.ndarray, model, feature_names: list = None, save_path: str = None
) -> pd.DataFrame:
    shap_importance = generate_shap_feature_importance(shap_values, feature_names)
    model_importance = generate_model_feature_importance(model, feature_names)

    if model_importance is None:
        return shap_importance

    comparison = pd.merge(
        shap_importance.rename(columns={"importance": "shap_importance"}),
        model_importance.rename(columns={"importance": "model_importance"}),
        on="feature",
        how="outer",
    ).fillna(0)

    comparison["shap_rank"] = (
        comparison["shap_importance"].rank(ascending=False).astype(int)
    )
    comparison["model_rank"] = (
        comparison["model_importance"].rank(ascending=False).astype(int)
    )
    comparison["rank_diff"] = comparison["model_rank"] - comparison["shap_rank"]

    comparison = comparison.sort_values("shap_importance", ascending=False)

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "feature_importance_comparison.csv")

    comparison.to_csv(save_path, index=False)
    logger.info(f"Feature importance comparison saved to {save_path}")

    return comparison


def plot_feature_importance_comparison(
    comparison_df: pd.DataFrame, save_path: str = None, top_n: int = 20
):
    comparison_df = comparison_df.head(top_n)

    fig, ax = plt.subplots(figsize=(12, 8))

    x = np.arange(len(comparison_df))
    width = 0.35

    ax.barh(
        x - width / 2, comparison_df["shap_importance"], width, label="SHAP", alpha=0.7
    )
    ax.barh(
        x + width / 2,
        comparison_df["model_importance"],
        width,
        label="Model Built-in",
        alpha=0.7,
    )

    ax.set_yticks(x)
    ax.set_yticklabels(comparison_df["feature"])
    ax.invert_yaxis()
    ax.set_xlabel("Importance")
    ax.set_title(f"Top {top_n} Feature Importance Comparison")
    ax.legend()

    plt.tight_layout()

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "feature_importance_comparison.png")

    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"Feature importance comparison plot saved to {save_path}")
    return save_path


def save_feature_importance(
    shap_values: np.ndarray,
    feature_names: list = None,
    save_csv: bool = True,
    save_json: bool = True,
):
    feature_importance = generate_shap_feature_importance(shap_values, feature_names)

    if save_csv:
        csv_path = os.path.join(MODEL_DIR, "feature_importance.csv")
        feature_importance.to_csv(csv_path, index=False)
        logger.info(f"Feature importance saved to {csv_path}")

    if save_json:
        json_path = os.path.join(MODEL_DIR, "feature_importance.json")
        feature_importance.head(20).to_json(json_path, orient="records", indent=2)
        logger.info(f"Feature importance saved to {json_path}")

    return feature_importance
