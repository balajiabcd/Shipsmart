import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def train_elasticnet_regression(
    X: pd.DataFrame, y: pd.Series, alpha: float = 1.0, l1_ratio: float = 0.5
) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42, max_iter=10000)
    model.fit(X_train_scaled, y_train)

    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "elasticnet_regression.joblib"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "elasticnet_scaler.joblib"))

    logger.info(f"ElasticNet - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}")

    return {
        "model": model,
        "scaler": scaler,
        "train_score": train_score,
        "test_score": test_score,
        "alpha": alpha,
        "l1_ratio": l1_ratio,
    }


def predict_elasticnet_regression(
    X: pd.DataFrame, model_path: str = None, scaler_path: str = None
) -> np.ndarray:
    if model_path is None:
        model_path = os.path.join(MODEL_DIR, "elasticnet_regression.joblib")
    if scaler_path is None:
        scaler_path = os.path.join(MODEL_DIR, "elasticnet_scaler.joblib")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)

    return predictions
