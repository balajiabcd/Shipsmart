import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
)
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def tune_ridge_regression(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}

    model = Ridge()
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "ridge_regression_tuned.joblib"))

    logger.info(
        f"Ridge Regression - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_lasso_regression(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}

    model = Lasso(max_iter=10000)
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "lasso_regression_tuned.joblib"))

    logger.info(
        f"Lasso Regression - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_elasticnet(X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5) -> dict:
    param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0], "l1_ratio": [0.2, 0.5, 0.8]}

    model = ElasticNet(max_iter=10000)
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "elasticnet_tuned.joblib"))

    logger.info(
        f"ElasticNet - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_random_forest_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, 20, None],
        "min_samples_split": [2, 5, 10],
    }

    model = RandomForestRegressor(random_state=42, n_jobs=-1)
    random_search = RandomizedSearchCV(
        model, param_grid, n_iter=20, cv=cv, scoring="r2", n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)

    best_model = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = random_search.best_score_

    joblib.dump(
        best_model, os.path.join(MODEL_DIR, "random_forest_regressor_tuned.joblib")
    )

    logger.info(
        f"Random Forest Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_gradient_boosting_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.1, 0.2],
    }

    model = GradientBoostingRegressor(random_state=42)
    random_search = RandomizedSearchCV(
        model, param_grid, n_iter=20, cv=cv, scoring="r2", n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)

    best_model = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = random_search.best_score_

    joblib.dump(
        best_model, os.path.join(MODEL_DIR, "gradient_boosting_regressor_tuned.joblib")
    )

    logger.info(
        f"Gradient Boosting Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_knn_regressor(X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5) -> dict:
    param_grid = {"n_neighbors": [3, 5, 7, 9, 11], "weights": ["uniform", "distance"]}

    model = KNeighborsRegressor()
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "knn_regressor_tuned.joblib"))

    logger.info(
        f"KNN Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_decision_tree_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "max_depth": [3, 5, 10, 20, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }

    model = DecisionTreeRegressor(random_state=42)
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    joblib.dump(
        best_model, os.path.join(MODEL_DIR, "decision_tree_regressor_tuned.joblib")
    )

    logger.info(
        f"Decision Tree Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_svr(X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5) -> dict:
    param_grid = {
        "C": [0.1, 1, 10],
        "epsilon": [0.01, 0.1, 0.2],
        "kernel": ["rbf", "linear"],
    }

    model = SVR()
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring="r2", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    joblib.dump(best_model, os.path.join(MODEL_DIR, "svr_tuned.joblib"))

    logger.info(f"SVR - Best params: {best_params}, Best CV R²: {best_score:.4f}")

    return {"model": best_model, "best_params": best_params, "best_score": best_score}


def tune_extra_trees_regressor(
    X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5
) -> dict:
    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, 20, None],
        "min_samples_split": [2, 5, 10],
    }

    model = ExtraTreesRegressor(random_state=42, n_jobs=-1)
    random_search = RandomizedSearchCV(
        model, param_grid, n_iter=20, cv=cv, scoring="r2", n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)

    best_model = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = random_search.best_score_

    joblib.dump(
        best_model, os.path.join(MODEL_DIR, "extra_trees_regressor_tuned.joblib")
    )

    logger.info(
        f"Extra Trees Regressor - Best params: {best_params}, Best CV R²: {best_score:.4f}"
    )

    return {"model": best_model, "best_params": best_params, "best_score": best_score}
