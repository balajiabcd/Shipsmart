import os
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.columns].values


def create_regression_pipeline(
    model, scaler_type: str = "standard", use_scaler: bool = True
) -> Pipeline:
    if use_scaler:
        if scaler_type == "standard":
            scaler = StandardScaler()
        elif scaler_type == "robust":
            scaler = RobustScaler()
        elif scaler_type == "minmax":
            scaler = MinMaxScaler()
        else:
            scaler = StandardScaler()

        pipeline = Pipeline([("scaler", scaler), ("model", model)])
    else:
        pipeline = Pipeline([("model", model)])

    return pipeline


def create_column_transform_pipeline(numeric_features: list, model) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[("num", StandardScaler(), numeric_features)]
    )

    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])

    return pipeline


def save_pipeline(pipeline, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(pipeline, filepath)
    logger.info(f"Pipeline saved to {filepath}")


def load_pipeline(filepath: str):
    return joblib.load(filepath)
