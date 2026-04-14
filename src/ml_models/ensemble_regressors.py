import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import VotingRegressor, StackingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
)
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def create_voting_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, voting_type: str = "hard"
) -> dict:
    estimators = [
        ("rf", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ("gb", GradientBoostingRegressor(n_estimators=100, random_state=42)),
        ("xgb", XGBRegressor(n_estimators=100, random_state=42, verbosity=0)),
        ("lgbm", LGBMRegressor(n_estimators=100, random_state=42, verbosity=-1)),
    ]

    model = VotingRegressor(estimators=estimators, voting=voting_type, n_jobs=-1)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)

    joblib.dump(model, os.path.join(MODEL_DIR, "voting_regressor.joblib"))

    logger.info(f"Voting Regressor - Train R²: {train_score:.4f}")

    return {"model": model, "train_score": train_score, "voting_type": voting_type}


def create_stacking_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, final_estimator=None
) -> dict:
    base_estimators = [
        ("rf", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ("gb", GradientBoostingRegressor(n_estimators=100, random_state=42)),
        ("xgb", XGBRegressor(n_estimators=100, random_state=42, verbosity=0)),
        ("lgbm", LGBMRegressor(n_estimators=100, random_state=42, verbosity=-1)),
    ]

    if final_estimator is None:
        final_estimator = Ridge(alpha=1.0)

    model = StackingRegressor(
        estimators=base_estimators, final_estimator=final_estimator, cv=5, n_jobs=-1
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)

    joblib.dump(model, os.path.join(MODEL_DIR, "stacking_regressor.joblib"))

    logger.info(f"Stacking Regressor - Train R²: {train_score:.4f}")

    return {"model": model, "train_score": train_score}


def create_weighted_voting_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, weights: list = None
) -> dict:
    if weights is None:
        weights = [1, 1, 2, 2]

    estimators = [
        ("rf", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ("et", ExtraTreesRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ("xgb", XGBRegressor(n_estimators=100, random_state=42, verbosity=0)),
        ("lgbm", LGBMRegressor(n_estimators=100, random_state=42, verbosity=-1)),
    ]

    model = VotingRegressor(estimators=estimators, weights=weights, n_jobs=-1)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)

    joblib.dump(model, os.path.join(MODEL_DIR, "weighted_voting_regressor.joblib"))

    logger.info(f"Weighted Voting Regressor - Train R²: {train_score:.4f}")

    return {"model": model, "train_score": train_score, "weights": weights}


def predict_ensemble_regressor(X: pd.DataFrame, model_path: str = None) -> np.ndarray:
    if model_path is None:
        model_path = os.path.join(MODEL_DIR, "stacking_regressor.joblib")

    model = joblib.load(model_path)
    predictions = model.predict(X)

    return predictions
