import pandas as pd
import numpy as np
import os
import logging
import joblib
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class RidgeRegressor:
    def __init__(self, alpha: float = 1.0, **kwargs):
        self.alpha = alpha
        self.model = None
        self.scaler = None
        self.training_metrics = {}

    def fit(
        self, X_train: pd.DataFrame, y_train: pd.Series, use_scaling: bool = True
    ) -> "RidgeRegressor":
        X_processed = X_train.fillna(0)

        if use_scaling:
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X_processed)
        else:
            X_scaled = X_processed.values

        self.model = Ridge(alpha=self.alpha)
        self.model.fit(X_scaled, y_train)

        train_pred = self.model.predict(X_scaled)
        self.training_metrics = {
            "train_rmse": np.sqrt(mean_squared_error(y_train, train_pred)),
            "train_mae": mean_absolute_error(y_train, train_pred),
            "train_r2": r2_score(y_train, train_pred),
        }

        logger.info(f"Training complete. Metrics: {self.training_metrics}")
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        X_processed = X.fillna(0)
        if self.scaler is not None:
            X_scaled = self.scaler.transform(X_processed)
        else:
            X_scaled = X_processed.values
        return self.model.predict(X_scaled)

    def evaluate(self, X_val: pd.DataFrame, y_val: pd.Series) -> Dict:
        y_pred = self.predict(X_val)
        return {
            "rmse": np.sqrt(mean_squared_error(y_val, y_pred)),
            "mae": mean_absolute_error(y_val, y_pred),
            "r2": r2_score(y_val, y_pred),
        }

    def save(self, model_path: str, scaler_path: Optional[str] = None) -> None:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")
        if self.scaler is not None and scaler_path:
            joblib.dump(self.scaler, scaler_path)


def train_ridge_model() -> Dict:
    try:
        X_train = pd.read_csv("data/ml/X_train.csv")
        y_train = pd.Series(np.random.exponential(10, len(X_train)))
        X_val = pd.read_csv("data/ml/X_val.csv")
        y_val = pd.Series(np.random.exponential(10, len(X_val)))
    except Exception as e:
        logger.warning(f"Using sample data: {e}")
        np.random.seed(42)
        X_train = pd.DataFrame({"f1": np.random.randn(500), "f2": np.random.randn(500)})
        y_train = pd.Series(np.random.exponential(10, 500))
        X_val = pd.DataFrame({"f1": np.random.randn(100), "f2": np.random.randn(100)})
        y_val = pd.Series(np.random.exponential(10, 100))

    model = RidgeRegressor(alpha=1.0)
    model.fit(X_train, y_train, use_scaling=True)

    train_metrics = model.evaluate(X_train, y_train)
    val_metrics = model.evaluate(X_val, y_val)

    print("\n=== Ridge Regression Results ===")
    print(f"Train - RMSE: {train_metrics['rmse']:.4f}, R²: {train_metrics['r2']:.4f}")
    print(f"Val   - RMSE: {val_metrics['rmse']:.4f}, R²: {val_metrics['r2']:.4f}")

    model.save("models/ridge_regression.pkl", "models/ridge_scaler.pkl")
    return {"model": model, "val_metrics": val_metrics}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = train_ridge_model()
