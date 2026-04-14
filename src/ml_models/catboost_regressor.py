import os
import joblib
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def train_catboost_regressor(
    X: pd.DataFrame,
    y: pd.Series,
    iterations: int = 100,
    depth: int = 6,
    learning_rate: float = 0.1,
) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = CatBoostRegressor(
        iterations=iterations,
        depth=depth,
        learning_rate=learning_rate,
        random_state=42,
        verbose=0,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "catboost_regressor.joblib"))

    logger.info(
        f"CatBoost Regressor - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}"
    )

    return {
        "model": model,
        "train_score": train_score,
        "test_score": test_score,
        "iterations": iterations,
        "depth": depth,
        "learning_rate": learning_rate,
    }


def predict_catboost_regressor(X: pd.DataFrame, model_path: str = None) -> np.ndarray:
    if model_path is None:
        model_path = os.path.join(MODEL_DIR, "catboost_regressor.joblib")

    model = joblib.load(model_path)
    predictions = model.predict(X)

    return predictions
