import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import lime
import lime.lime_tabular
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
LIME_PLOTS_DIR = os.path.join(MODEL_DIR, "lime_plots")
os.makedirs(LIME_PLOTS_DIR, exist_ok=True)


def create_local_explanation_visualization(
    explainer,
    instance: np.ndarray,
    predict_fn,
    save_path: str = None,
    num_features: int = 10,
):
    exp = explainer.explain_instance(instance, predict_fn, num_features=num_features)

    if save_path is None:
        save_path = os.path.join(LIME_PLOTS_DIR, "explanation.png")

    fig = exp.as_pyplot_figure()
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"Local explanation saved to {save_path}")
    return save_path


def create_batch_local_explanations(
    model,
    X: pd.DataFrame,
    n_samples: int = 10,
    num_features: int = 10,
    class_names: list = None,
    save_dir: str = None,
):
    if class_names is None:
        class_names = ["OnTime", "Delayed"]

    if save_dir is None:
        save_dir = LIME_PLOTS_DIR

    os.makedirs(save_dir, exist_ok=True)

    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X.values,
        feature_names=X.columns.tolist(),
        class_names=class_names,
        mode="classification",
    )

    predict_fn = model.predict_proba

    saved_plots = []
    for i in range(min(n_samples, len(X))):
        save_path = os.path.join(save_dir, f"explanation_{i}.png")

        exp = explainer.explain_instance(
            X.iloc[i].values, predict_fn, num_features=num_features
        )
        fig = exp.as_pyplot_figure()
        plt.tight_layout()
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()

        saved_plots.append(save_path)

        if (i + 1) % 10 == 0:
            logger.info(f"Created {i + 1} local explanations")

    logger.info(f"Created {len(saved_plots)} local explanation plots")
    return saved_plots


def aggregate_lime_explanations(explanations: list) -> pd.DataFrame:
    feature_importance = {}

    for exp in explanations:
        for feature, value in exp.get("features", []):
            if feature not in feature_importance:
                feature_importance[feature] = []
            feature_importance[feature].append(abs(value))

    aggregated = []
    for feature, values in feature_importance.items():
        aggregated.append(
            {
                "feature": feature,
                "mean_importance": np.mean(values),
                "std_importance": np.std(values),
                "count": len(values),
            }
        )

    aggregated_df = pd.DataFrame(aggregated).sort_values(
        "mean_importance", ascending=False
    )

    return aggregated_df


def compare_shap_lime(shap_explanations: list, lime_explanations: list) -> dict:
    shap_features = set([f for exp in shap_explanations for f, v in exp])
    lime_features = set(
        [f for exp in lime_explanations for f, v in exp.get("features", [])]
    )

    common_features = shap_features & lime_features
    only_shap = shap_features - lime_features
    only_lime = lime_features - shap_features

    return {
        "common_features": list(common_features),
        "only_shap": list(only_shap),
        "only_lime": list(only_lime),
        "agreement": len(common_features) / max(len(shap_features | lime_features), 1),
    }
