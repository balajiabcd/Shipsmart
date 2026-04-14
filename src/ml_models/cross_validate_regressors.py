import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
)
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cross_validate_regressor(model, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> dict:
    kfold = KFold(n_splits=cv, shuffle=True, random_state=42)

    r2_scores = cross_val_score(model, X, y, cv=kfold, scoring="r2")
    neg_mae_scores = cross_val_score(
        model, X, y, cv=kfold, scoring="neg_mean_absolute_error"
    )
    neg_mse_scores = cross_val_score(
        model, X, y, cv=kfold, scoring="neg_mean_squared_error"
    )

    return {
        "r2_mean": r2_scores.mean(),
        "r2_std": r2_scores.std(),
        "mae_mean": -neg_mae_scores.mean(),
        "mae_std": neg_mae_scores.std(),
        "rmse_mean": np.sqrt(-neg_mse_scores.mean()),
        "rmse_std": np.sqrt(neg_mse_scores.std()),
        "cv_scores": r2_scores,
    }


def cv_all_regressors(X: pd.DataFrame, y: pd.Series, cv: int = 5) -> pd.DataFrame:
    models = {
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(max_iter=10000),
        "ElasticNet": ElasticNet(max_iter=10000),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            n_estimators=100, random_state=42
        ),
        "KNN Regressor": KNeighborsRegressor(),
        "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
        "SVR": SVR(),
        "Extra Trees Regressor": ExtraTreesRegressor(
            n_estimators=100, random_state=42, n_jobs=-1
        ),
        "XGBoost Regressor": XGBRegressor(
            n_estimators=100, random_state=42, verbosity=0
        ),
        "LightGBM Regressor": LGBMRegressor(
            n_estimators=100, random_state=42, verbosity=-1
        ),
        "CatBoost Regressor": CatBoostRegressor(
            n_estimators=100, random_state=42, verbose=0
        ),
    }

    results = []

    for model_name, model in models.items():
        try:
            cv_results = cross_validate_regressor(model, X, y, cv)
            results.append(
                {
                    "Model": model_name,
                    "R2_Mean": cv_results["r2_mean"],
                    "R2_Std": cv_results["r2_std"],
                    "MAE_Mean": cv_results["mae_mean"],
                    "MAE_Std": cv_results["mae_std"],
                    "RMSE_Mean": cv_results["rmse_mean"],
                    "RMSE_Std": cv_results["rmse_std"],
                }
            )
            logger.info(
                f"{model_name} - CV R²: {cv_results['r2_mean']:.4f} (+/- {cv_results['r2_std']:.4f})"
            )
        except Exception as e:
            logger.error(f"Error cross-validating {model_name}: {e}")

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("R2_Mean", ascending=False)

    return results_df


def cv_with_stratified_bins(
    X: pd.DataFrame, y: pd.Series, n_bins: int = 5, cv: int = 5
) -> dict:
    y_binned = pd.qcut(y, q=n_bins, labels=False, duplicates="drop")

    kfold = KFold(n_splits=cv, shuffle=True, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    r2_scores = cross_val_score(model, X, y, cv=kfold, scoring="r2")

    return {
        "r2_mean": r2_scores.mean(),
        "r2_std": r2_scores.std(),
        "cv_scores": r2_scores,
    }
