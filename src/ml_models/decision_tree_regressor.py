import os
import joblib
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def train_decision_tree_regressor(
    X: pd.DataFrame, y: pd.Series, max_depth: int = None, min_samples_split: int = 2
) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeRegressor(
        max_depth=max_depth, min_samples_split=min_samples_split, random_state=42
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "decision_tree_regressor.joblib"))

    logger.info(
        f"Decision Tree Regressor - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}"
    )

    return {
        "model": model,
        "train_score": train_score,
        "test_score": test_score,
        "max_depth": max_depth,
        "min_samples_split": min_samples_split,
    }


def predict_decision_tree_regressor(
    X: pd.DataFrame, model_path: str = None
) -> np.ndarray:
    if model_path is None:
        model_path = os.path.join(MODEL_DIR, "decision_tree_regressor.joblib")

    model = joblib.load(model_path)
    predictions = model.predict(X)

    return predictions
