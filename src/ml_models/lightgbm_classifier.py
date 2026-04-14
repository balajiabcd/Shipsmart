import pandas as pd
import numpy as np
import os
import logging
import joblib
import lightgbm as lgb
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    classification_report,
)
from sklearn.model_selection import cross_val_score
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class LightGBMClassifier:
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        num_leaves: int = 31,
        subsample: float = 1.0,
        colsample_bytree: float = 1.0,
        random_state: int = 42,
        **kwargs,
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.num_leaves = num_leaves
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.random_state = random_state
        self.model = None
        self.feature_importances_ = None
        self.training_metrics = {}

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> "LightGBMClassifier":
        """Train LightGBM model."""
        X_processed = X_train.fillna(0)

        self.model = lgb.LGBMClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            num_leaves=self.num_leaves,
            subsample=self.subsample,
            colsample_bytree=self.colsample_bytree,
            random_state=self.random_state,
            verbose=-1,
        )
        self.model.fit(X_processed, y_train)

        self.feature_importances_ = pd.DataFrame(
            {
                "feature": X_processed.columns,
                "importance": self.model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        train_pred = self.model.predict(X_processed)
        train_proba = self.model.predict_proba(X_processed)[:, 1]

        self.training_metrics = {
            "train_accuracy": accuracy_score(y_train, train_pred),
            "train_f1": f1_score(y_train, train_pred),
            "train_roc_auc": roc_auc_score(y_train, train_proba),
        }

        logger.info(f"Training complete. Metrics: {self.training_metrics}")

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict class labels."""
        X_processed = X.fillna(0)
        return self.model.predict(X_processed)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict class probabilities."""
        X_processed = X.fillna(0)
        return self.model.predict_proba(X_processed)

    def evaluate(self, X_val: pd.DataFrame, y_val: pd.Series) -> Dict:
        """Evaluate model on validation set."""
        y_pred = self.predict(X_val)
        y_proba = self.predict_proba(X_val)[:, 1]

        return {
            "accuracy": accuracy_score(y_val, y_pred),
            "f1": f1_score(y_val, y_pred),
            "precision": precision_score(y_val, y_pred, zero_division=0),
            "recall": recall_score(y_val, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_val, y_proba),
        }

    def get_top_features(self, n: int = 10) -> pd.DataFrame:
        """Get top N most important features."""
        if self.feature_importances_ is not None:
            return self.feature_importances_.head(n)
        return pd.DataFrame()

    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict:
        """Perform cross-validation."""
        X_processed = X.fillna(0)

        model = lgb.LGBMClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            random_state=self.random_state,
            verbose=-1,
        )

        cv_scores = cross_val_score(model, X_processed, y, cv=cv, scoring="f1")

        return {
            "cv_scores": cv_scores,
            "mean_f1": cv_scores.mean(),
            "std_f1": cv_scores.std(),
        }

    def save(self, model_path: str) -> None:
        """Save model to disk."""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")

        if self.feature_importances_ is not None:
            importance_path = model_path.replace(".pkl", "_importances.csv")
            self.feature_importances_.to_csv(importance_path, index=False)

    def load(self, model_path: str) -> None:
        """Load model from disk."""
        self.model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")


def train_lightgbm_model() -> Dict:
    """Train LightGBM model."""

    try:
        X_train = pd.read_csv("data/ml/X_train.csv")
        y_train = pd.read_csv("data/ml/y_train_class.csv")["is_delayed"]
        X_val = pd.read_csv("data/ml/X_val.csv")
        y_val = pd.read_csv("data/ml/y_val_class.csv")["is_delayed"]
    except Exception as e:
        logger.warning(f"Could not load split data: {e}. Using sample data.")

        np.random.seed(42)
        n_samples = 1000
        X_train = pd.DataFrame(
            {
                "feature1": np.random.randn(n_samples),
                "feature2": np.random.randn(n_samples),
                "feature3": np.random.randint(0, 5, n_samples),
                "feature4": np.random.randn(n_samples),
                "feature5": np.random.randn(n_samples),
            }
        )
        y_train = pd.Series(np.random.randint(0, 2, n_samples))

        X_val = pd.DataFrame(
            {
                "feature1": np.random.randn(200),
                "feature2": np.random.randn(200),
                "feature3": np.random.randint(0, 5, 200),
                "feature4": np.random.randn(200),
                "feature5": np.random.randn(200),
            }
        )
        y_val = pd.Series(np.random.randint(0, 2, 200))

    model = LightGBMClassifier(
        n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)

    train_metrics = model.evaluate(X_train, y_train)
    val_metrics = model.evaluate(X_val, y_val)

    print("\n=== LightGBM Results ===")
    print(
        f"Train - Accuracy: {train_metrics['accuracy']:.4f}, F1: {train_metrics['f1']:.4f}"
    )
    print(
        f"Val   - Accuracy: {val_metrics['accuracy']:.4f}, F1: {val_metrics['f1']:.4f}, ROC-AUC: {val_metrics['roc_auc']:.4f}"
    )

    print("\nTop 10 Feature Importances:")
    print(model.get_top_features(10))

    model.save("models/lightgbm_classifier.pkl")

    return {"model": model, "train_metrics": train_metrics, "val_metrics": val_metrics}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = train_lightgbm_model()
