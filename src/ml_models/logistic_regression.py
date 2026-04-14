import pandas as pd
import numpy as np
import os
import logging
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import cross_val_score
from typing import Tuple, Dict, Optional

logger = logging.getLogger(__name__)


class LogisticRegressionClassifier:
    def __init__(self, max_iter: int = 1000, random_state: int = 42, **kwargs):
        self.max_iter = max_iter
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.feature_names = None
        self.training_metrics = {}

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess data - handle missing values and encoding."""
        df = df.copy()

        for col in df.columns:
            if df[col].dtype == "object":
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(
                        df[col].astype(str)
                    )
                else:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))

        df = df.fillna(0)

        return df

    def fit(
        self, X_train: pd.DataFrame, y_train: pd.Series, use_scaling: bool = True
    ) -> "LogisticRegressionClassifier":
        """Train logistic regression model.

        Args:
            X_train: Training features
            y_train: Training labels
            use_scaling: Whether to scale features

        Returns:
            self
        """
        X_processed = self._preprocess(X_train)
        self.feature_names = list(X_processed.columns)

        if use_scaling:
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_processed)
        else:
            X_train_scaled = X_processed.values

        self.model = LogisticRegression(
            max_iter=self.max_iter, random_state=self.random_state
        )
        self.model.fit(X_train_scaled, y_train)

        train_pred = self.model.predict(X_train_scaled)
        train_proba = self.model.predict_proba(X_train_scaled)[:, 1]

        self.training_metrics = {
            "train_accuracy": accuracy_score(y_train, train_pred),
            "train_f1": f1_score(y_train, train_pred),
            "train_roc_auc": roc_auc_score(y_train, train_proba),
        }

        logger.info(f"Training metrics: {self.training_metrics}")

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict class labels."""
        X_processed = self._preprocess(X)

        if self.scaler is not None:
            X_scaled = self.scaler.transform(X_processed)
        else:
            X_scaled = X_processed.values

        return self.model.predict(X_scaled)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict class probabilities."""
        X_processed = self._preprocess(X)

        if self.scaler is not None:
            X_scaled = self.scaler.transform(X_processed)
        else:
            X_scaled = X_processed.values

        return self.model.predict_proba(X_scaled)

    def evaluate(self, X_val: pd.DataFrame, y_val: pd.Series) -> Dict:
        """Evaluate model on validation set.

        Args:
            X_val: Validation features
            y_val: Validation labels

        Returns:
            Dictionary of metrics
        """
        y_pred = self.predict(X_val)
        y_proba = self.predict_proba(X_val)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_val, y_pred),
            "f1": f1_score(y_val, y_pred),
            "precision": precision_score(y_val, y_pred, zero_division=0),
            "recall": recall_score(y_val, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_val, y_proba),
        }

        return metrics

    def get_classification_report(self, X_val: pd.DataFrame, y_val: pd.Series) -> str:
        """Get detailed classification report."""
        y_pred = self.predict(X_val)
        return classification_report(y_val, y_pred)

    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict:
        """Perform cross-validation.

        Args:
            X: Features
            y: Labels
            cv: Number of folds

        Returns:
            Cross-validation results
        """
        X_processed = self._preprocess(X)

        if self.scaler is not None:
            X_scaled = self.scaler.fit_transform(X_processed)
        else:
            X_scaled = X_processed.values

        model = LogisticRegression(
            max_iter=self.max_iter, random_state=self.random_state
        )

        cv_scores = cross_val_score(model, X_scaled, y, cv=cv, scoring="f1")

        return {
            "cv_scores": cv_scores,
            "mean_f1": cv_scores.mean(),
            "std_f1": cv_scores.std(),
        }

    def save(self, model_path: str, scaler_path: Optional[str] = None) -> None:
        """Save model and scaler to disk.

        Args:
            model_path: Path to save model
            scaler_path: Path to save scaler
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")

        if self.scaler is not None and scaler_path:
            joblib.dump(self.scaler, scaler_path)
            logger.info(f"Scaler saved to {scaler_path}")

    def load(self, model_path: str, scaler_path: Optional[str] = None) -> None:
        """Load model and scaler from disk.

        Args:
            model_path: Path to model
            scaler_path: Path to scaler
        """
        self.model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")

        if scaler_path and os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")


def train_logistic_regression_model() -> Dict:
    """Train logistic regression model with sample data."""

    try:
        X_train = pd.read_csv("data/ml/X_train.csv")
        y_train = pd.read_csv("data/ml/y_train_class.csv")
        X_val = pd.read_csv("data/ml/X_val.csv")
        y_val = pd.read_csv("data/ml/y_val_class.csv")

        if "is_delayed" in y_train.columns:
            y_train = y_train["is_delayed"]
        if "is_delayed" in y_val.columns:
            y_val = y_val["is_delayed"]

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

    model = LogisticRegressionClassifier(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    train_metrics = model.evaluate(X_train, y_train)
    val_metrics = model.evaluate(X_val, y_val)

    print("\n=== Logistic Regression Results ===")
    print(
        f"Train - Accuracy: {train_metrics['accuracy']:.4f}, F1: {train_metrics['f1']:.4f}"
    )
    print(
        f"Val   - Accuracy: {val_metrics['accuracy']:.4f}, F1: {val_metrics['f1']:.4f}, ROC-AUC: {val_metrics['roc_auc']:.4f}"
    )

    model.save(
        "models/logistic_regression.pkl", "models/logistic_regression_scaler.pkl"
    )

    return {"model": model, "train_metrics": train_metrics, "val_metrics": val_metrics}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = train_logistic_regression_model()
