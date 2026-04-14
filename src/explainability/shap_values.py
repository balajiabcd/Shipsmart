import os
import numpy as np
import pandas as pd
import joblib
import shap
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


def generate_shap_values(
    model_name: str = None, model=None, X: pd.DataFrame = None, save: bool = True
):
    if model is None:
        if model_name is None:
            model_files = [
                f
                for f in os.listdir(MODEL_DIR)
                if f.endswith(".joblib") and "classifier" in f
            ]
            if not model_files:
                raise ValueError("No classifier model found")
            model_name = model_files[0]

        model_path = os.path.join(MODEL_DIR, model_name)
        model = joblib.load(model_path)
        logger.info(f"Loaded model: {model_name}")

    if X is None:
        raise ValueError("Feature data (X) is required")

    X = X.fillna(0)

    if hasattr(model, "predict_proba"):
        try:
            if hasattr(shap, "TreeExplainer"):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X)
            else:
                logger.warning("TreeExplainer not available, using linear explainer")
                from shap import KernelExplainer

                def predict_proba(x):
                    return model.predict_proba(x)[:, 1]

                explainer = KernelExplainer(predict_proba, X.iloc[:50])
                shap_values = explainer.shap_values(X)
        except Exception as e:
            logger.error(f"Error generating SHAP values: {e}")
            raise
    else:
        logger.warning("Model doesn't have predict_proba, using prediction directly")

        def predict_fn(x):
            return model.predict(x)

        explainer = shap.KernelExplainer(predict_fn, X.iloc[:50])
        shap_values = explainer.shap_values(X)

    logger.info(f"SHAP values shape: {shap_values.shape}")

    if save:
        shap_path = os.path.join(MODEL_DIR, "shap_values.npy")
        np.save(shap_path, shap_values)
        logger.info(f"SHAP values saved to {shap_path}")

    return shap_values, explainer


def load_shap_values(filepath: str = None):
    if filepath is None:
        filepath = os.path.join(MODEL_DIR, "shap_values.npy")

    shap_values = np.load(filepath)
    logger.info(f"Loaded SHAP values shape: {shap_values.shape}")
    return shap_values


def get_expected_value(explainer):
    if hasattr(explainer, "expected_value"):
        expected_value = explainer.expected_value
        if isinstance(expected_value, (list, np.ndarray)):
            return expected_value[1] if len(expected_value) > 1 else expected_value[0]
        return expected_value
    return None
