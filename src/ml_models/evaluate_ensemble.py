import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_ensemble_regressor(
    X_test: pd.DataFrame, y_test: pd.Series, model_path: str = None
) -> dict:
    if model_path is None:
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "stacking_regressor.joblib"
        )

    model = joblib.load(model_path)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results = {"MSE": mse, "RMSE": rmse, "MAE": mae, "R2": r2}

    logger.info(f"Ensemble Regressor - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")

    return results


def compare_with_baseline(y_test: pd.Series, y_pred: pd.Series) -> dict:
    baseline_pred = np.full_like(y_test, y_test.mean())

    baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
    model_rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    improvement = ((baseline_rmse - model_rmse) / baseline_rmse) * 100

    return {
        "baseline_rmse": baseline_rmse,
        "model_rmse": model_rmse,
        "improvement_percent": improvement,
    }
