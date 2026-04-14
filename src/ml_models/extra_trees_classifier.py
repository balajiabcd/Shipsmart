import pandas as pd
import numpy as np
import os
import logging
import joblib
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from typing import Dict

logger = logging.getLogger(__name__)


class ExtraTreesClassifierModel:
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        random_state: int = 42,
        n_jobs: int = -1,
        **kwargs,
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.model = None
        self.feature_importances_ = None
        self.training_metrics = {}

    def fit(
        self, X_train: pd.DataFrame, y_train: pd.Series
    ) -> "ExtraTreesClassifierModel":
        """Train Extra Trees model."""
        X_processed = X_train.fillna(0)

        self.model = ExtraTreesClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            random_state=self.random_state,
            n_jobs=self.n_jobs,
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

    def save(self, model_path: str) -> None:
        """Save model to disk."""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")


def train_extra_trees_model() -> Dict:
    """Train Extra Trees model."""

    try:
        X_train = pd.read_csv("data/ml/X_train.csv")
        y_train = pd.read_csv("data/ml/y_train_class.csv")["is_delayed"]
        X_val = pd.read_csv("data/ml/X_val.csv")
        y_val = pd.read_csv("data/ml/y_val_class.csv")["is_delayed"]
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
        y_train = pd.Series(np.random.randint(0, 2, n_samples))

        X_val = pd.DataFrame(
            {
                "feature1": np.random.randn(100),
                "feature2": np.random.randn(100),
                "feature3": np.random.randint(0, 5, 100),
                "feature4": np.random.randn(100),
                "feature5": np.random.randn(100),
            }
        )
        y_val = pd.Series(np.random.randint(0, 2, 100))

    model = ExtraTreesClassifierModel(
        n_estimators=100, max_depth=None, random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)

    train_metrics = model.evaluate(X_train, y_train)
    val_metrics = model.evaluate(X_val, y_val)

    print("\n=== Extra Trees Results ===")
    print(
        f"Train - Accuracy: {train_metrics['accuracy']:.4f}, F1: {train_metrics['f1']:.4f}"
    )
    print(
        f"Val   - Accuracy: {val_metrics['accuracy']:.4f}, F1: {val_metrics['f1']:.4f}, ROC-AUC: {val_metrics['roc_auc']:.4f}"
    )

    model.save("models/extra_trees.pkl")

    return {"model": model, "train_metrics": train_metrics, "val_metrics": val_metrics}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = train_extra_trees_model()
