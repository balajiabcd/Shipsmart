import os
import json
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


def create_lime_explainer(
    X: pd.DataFrame, class_names: list = None, mode: str = "classification"
):
    if class_names is None:
        class_names = ["OnTime", "Delayed"]

    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X.values,
        feature_names=X.columns.tolist(),
        class_names=class_names,
        mode=mode,
    )

    logger.info("LIME explainer created")
    return explainer


def generate_lime_explanation(
    explainer, instance: np.ndarray, predict_fn, num_features: int = 10
):
    exp = explainer.explain_instance(instance, predict_fn, num_features=num_features)

    explanation = {
        "prediction": exp.predict,
        "probability": exp.predict_proba,
        "features": exp.as_list(),
    }

    return explanation, exp


def generate_batch_lime_explanations(
    model,
    X: pd.DataFrame,
    n_samples: int = 10,
    num_features: int = 10,
    class_names: list = None,
):
    if class_names is None:
        class_names = ["OnTime", "Delayed"]

    explainer = create_lime_explainer(X, class_names)

    predict_fn = model.predict_proba

    explanations = []
    for i in range(min(n_samples, len(X))):
        explanation, _ = generate_lime_explanation(
            explainer, X.iloc[i].values, predict_fn, num_features
        )
        explanations.append(
            {
                "sample_id": i,
                "prediction": explanation["prediction"],
                "probability": explanation["probability"].tolist(),
                "features": explanation["features"],
            }
        )

        if (i + 1) % 10 == 0:
            logger.info(f"Generated {i + 1} explanations")

    logger.info(f"Generated {len(explanations)} LIME explanations")
    return explanations


def save_lime_explanations(explanations: list, filepath: str = None):
    if filepath is None:
        filepath = os.path.join(MODEL_DIR, "lime_explanations.json")

    with open(filepath, "w") as f:
        json.dump(explanations, f, indent=2)

    logger.info(f"LIME explanations saved to {filepath}")
    return filepath


def load_lime_explanations(filepath: str = None) -> list:
    if filepath is None:
        filepath = os.path.join(MODEL_DIR, "lime_explanations.json")

    with open(filepath, "r") as f:
        explanations = json.load(f)

    logger.info(f"Loaded {len(explanations)} LIME explanations")
    return explanations


def create_lime_visualization(
    explainer,
    instance: np.ndarray,
    predict_fn,
    save_path: str = None,
    num_features: int = 10,
):
    exp = explainer.explain_instance(instance, predict_fn, num_features=num_features)

    if save_path is None:
        save_path = os.path.join(MODEL_DIR, "lime_explanation.png")

    exp.save_to_file(save_path)

    logger.info(f"LIME visualization saved to {save_path}")
    return save_path
