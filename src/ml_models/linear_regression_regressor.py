import pandas as pd
import numpy as np
import os
import logging
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class LinearRegressionRegressor:
    def __init__(self, **kwargs):
        self.model = None
        self.scaler = None
        self.training_metrics = {}

    def fit(
        self, X_train: pd.DataFrame, y_train: pd.Series, use_scaling: bool = True
    ) -> "LinearRegressionRegressor":
        """Train Linear Regression model."""
        X_processed = X_train.fillna(0)

        if use_scaling:
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X_processed)
        else:
            X_scaled = X_processed.values

        self.model = LinearRegression()
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
        """Predict delay minutes."""
        X_processed = X.fillna(0)

        if self.scaler is not None:
            X_scaled = self.scaler.transform(X_processed)
        else:
            X_scaled = X_processed.values

        return self.model.predict(X_scaled)

    def evaluate(self, X_val: pd.DataFrame, y_val: pd.Series) -> Dict:
        """Evaluate model on validation set."""
        y_pred = self.predict(X_val)

        return {
            "rmse": np.sqrt(mean_squared_error(y_val, y_pred)),
            "mae": mean_absolute_error(y_val, y_pred),
            "r2": r2_score(y_val, y_pred),
        }

    def save(self, model_path: str, scaler_path: Optional[str] = None) -> None:
        """Save model to disk."""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")

        if self.scaler is not None and scaler_path:
            joblib.dump(self.scaler, scaler_path)

    def load(self, model_path: str, scaler_path: Optional[str] = None) -> None:
        """Load model from disk."""
        self.model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")

        if scaler_path and os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)


def train_linear_regression_model() -> Dict:
    """Train Linear Regression model."""

    try:
        X_train = pd.read_csv("data/ml/X_train.csv")
        y_train = (
            pd.read_csv("data/ml/y_train_reg.csv")["delay_minutes"]
            if "y_train_reg.csv" in os.listdir("data/ml")
            else pd.read_csv("data/ml/y_train_class.csv")["is_delayed"]
        )
        X_val = pd.read_csv("data/ml/X_val.csv")
        y_val = (
            pd.read_csv("data/ml/y_val_reg.csv")["delay_minutes"]
            if "y_val_reg.csv" in os.listdir("data/ml")
            else pd.read_csv("data/ml/y_val_class.csv")["is_delayed"]
        )
    except Exception as e:
        logger.warning(f"Could not load split data: {e}. Using sample data.")

        np.random.seed(42)
        n_samples = 500
        X_train = pd.DataFrame(
            {
                "feature1": np.random.randn(n_samples),
                "feature2": np.random.randn(n_samples),
                "feature3": np.random.randint(0, 5, n_samples),
                "feature4": np.random.randn(n_samples),
                "feature5": np.random.randn(n_samples),
            }
        )
        y_train = pd.Series(np.random.exponential(10, n_samples))

        X_val = pd.DataFrame(
            {
                "feature1": np.random.randn(100),
                "feature2": np.random.randn(100),
                "feature3": np.random.randint(0, 5, 100),
                "feature4": np.random.randn(100),
                "feature5": np.random.randn(100),
            }
        )
        y_val = pd.Series(np.random.exponential(10, 100))

    model = LinearRegressionRegressor()
    model.fit(X_train, y_train, use_scaling=True)

    train_metrics = model.evaluate(X_train, y_train)
    val_metrics = model.evaluate(X_val, y_val)

    print("\n=== Linear Regression Results ===")
    print(
        f"Train - RMSE: {train_metrics['rmse']:.4f}, MAE: {train_metrics['mae']:.4f}, R²: {train_metrics['r2']:.4f}"
    )
    print(
        f"Val   - RMSE: {val_metrics['rmse']:.4f}, MAE: {val_metrics['mae']:.4f}, R²: {val_metrics['r2']:.4f}"
    )

    model.save(
        "models/linear_regression_reg.pkl", "models/linear_regression_reg_scaler.pkl"
    )

    return {"model": model, "train_metrics": train_metrics, "val_metrics": val_metrics}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = train_linear_regression_model()
