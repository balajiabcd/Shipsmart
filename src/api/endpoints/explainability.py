from fastapi import APIRouter, HTTPException
import os
import joblib
import pandas as pd
import numpy as np
import shap
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/explain", tags=["Explainability"])

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

model = None
explainer = None


def load_model_and_explainer():
    global model, explainer

    if model is None:
        model_files = [
            f
            for f in os.listdir(MODEL_DIR)
            if f.endswith(".joblib") and "classifier" in f
        ]
        if not model_files:
            raise HTTPException(status_code=500, detail="No classifier model found")

        model_path = os.path.join(MODEL_DIR, model_files[0])
        model = joblib.load(model_path)

        explainer = shap.TreeExplainer(model)

        logger.info(f"Loaded model: {model_files[0]}")

    return model, explainer


@router.post("/shap")
async def explain_with_shap(features: dict):
    """Return SHAP values for a single prediction"""
    try:
        model, explainer = load_model_and_explainer()

        df = pd.DataFrame([features])

        shap_values = explainer.shap_values(df)

        expected_value = explainer.expected_value
        if isinstance(expected_value, (list, np.ndarray)):
            expected_value = (
                expected_value[0] if len(expected_value) > 1 else expected_value
            )

        return {
            "shap_values": shap_values[0].tolist()
            if isinstance(shap_values, list)
            else shap_values.tolist(),
            "base_value": float(expected_value),
            "prediction": int(model.predict(df)[0]),
            "prediction_proba": model.predict_proba(df)[0].tolist()
            if hasattr(model, "predict_proba")
            else None,
        }
    except Exception as e:
        logger.error(f"Error generating SHAP explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feature-importance")
async def get_feature_importance():
    """Return global feature importance"""
    try:
        importance_path = os.path.join(MODEL_DIR, "feature_importance.csv")

        if not os.path.exists(importance_path):
            raise HTTPException(status_code=404, detail="Feature importance not found")

        importance = pd.read_csv(importance_path)

        return importance.head(20).to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading feature importance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/shap-batch")
async def explain_batch_shap(features_list: list):
    """Return SHAP values for multiple predictions"""
    try:
        model, explainer = load_model_and_explainer()

        df = pd.DataFrame(features_list)

        shap_values = explainer.shap_values(df)

        expected_value = explainer.expected_value
        if isinstance(expected_value, (list, np.ndarray)):
            expected_value = expected_value[0]

        predictions = model.predict(df)

        return {
            "shap_values": shap_values.tolist(),
            "base_value": float(expected_value),
            "predictions": predictions.tolist()
            if hasattr(predictions, "tolist")
            else predictions,
        }
    except Exception as e:
        logger.error(f"Error generating batch SHAP explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-info")
async def get_model_info():
    """Return model information and explanation method"""
    try:
        model, explainer = load_model_and_explainer()

        expected_value = explainer.expected_value
        if isinstance(expected_value, (list, np.ndarray)):
            expected_value = expected_value[0]

        return {
            "model_type": type(model).__name__,
            "explainer_type": type(explainer).__name__,
            "base_value": float(expected_value),
            "features_count": len(model.feature_importances_)
            if hasattr(model, "feature_importances_")
            else None,
        }
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
