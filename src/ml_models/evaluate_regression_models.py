import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


def evaluate_regression_models(X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    models = {
        "Linear Regression": "linear_regression_regressor.joblib",
        "Ridge Regression": "ridge_regression_regressor.joblib",
        "Lasso Regression": "lasso_regression.joblib",
        "ElasticNet": "elasticnet_regression.joblib",
        "Random Forest Regressor": "random_forest_regressor.joblib",
        "XGBoost Regressor": "xgboost_regressor.joblib",
        "LightGBM Regressor": "lightgbm_regressor.joblib",
        "CatBoost Regressor": "catboost_regressor.joblib",
        "SVR": "svr.joblib",
        "KNN Regressor": "knn_regressor.joblib",
        "Decision Tree Regressor": "decision_tree_regressor.joblib",
        "Gradient Boosting Regressor": "gradient_boosting_regressor.joblib",
        "Extra Trees Regressor": "extra_trees_regressor.joblib",
    }

    results = []

    for model_name, model_file in models.items():
        model_path = os.path.join(MODEL_DIR, model_file)

        if not os.path.exists(model_path):
            logger.warning(f"Model {model_name} not found at {model_path}")
            continue

        try:
            model = joblib.load(model_path)

            scaler_path = model_path.replace(".joblib", "_scaler.joblib")
            if os.path.exists(scaler_path):
                scaler = joblib.load(scaler_path)
                X_test_scaled = scaler.transform(X_test)
                y_pred = model.predict(X_test_scaled)
            else:
                y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            results.append(
                {"Model": model_name, "MSE": mse, "RMSE": rmse, "MAE": mae, "R2": r2}
            )

            logger.info(
                f"{model_name} - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}"
            )

        except Exception as e:
            logger.error(f"Error evaluating {model_name}: {e}")

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("R2", ascending=False)

    return results_df


def get_best_regressor(results_df: pd.DataFrame) -> str:
    if results_df.empty:
        return None

    best_model = results_df.iloc[0]["Model"]
    return best_model
