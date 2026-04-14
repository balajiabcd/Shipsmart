import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def tune_xgboost_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "n_estimators": [50, 100, 200, 300],
        "max_depth": [3, 5, 7, 10],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
        "min_child_weight": [1, 3, 5],
    }

    model = XGBRegressor(random_state=42, n_jobs=-1, verbosity=0)
    random_search = RandomizedSearchCV(
        model, param_grid, n_iter=30, cv=cv, scoring="r2", n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)

    best_model = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = random_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "xgboost_regressor_tuned.joblib"))

    logger.info(
        f"XGBoost Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_lightgbm_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "n_estimators": [50, 100, 200, 300],
        "max_depth": [3, 5, 7, 10, -1],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "num_leaves": [15, 31, 63, 127],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
    }

    model = LGBMRegressor(random_state=42, n_jobs=-1, verbosity=-1)
    random_search = RandomizedSearchCV(
        model, param_grid, n_iter=30, cv=cv, scoring="r2", n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)

    best_model = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = random_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "lightgbm_regressor_tuned.joblib"))

    logger.info(
        f"LightGBM Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_catboost_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "iterations": [50, 100, 200, 300],
        "depth": [4, 6, 8, 10],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "l2_leaf_reg": [1, 3, 5, 7],
    }

    model = CatBoostRegressor(random_state=42, verbose=0)
    random_search = RandomizedSearchCV(
        model, param_grid, n_iter=20, cv=cv, scoring="r2", n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)

    best_model = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = random_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "catboost_regressor_tuned.joblib"))

    logger.info(
        f"CatBoost Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}
