from typing import Optional
import pandas as pd
import numpy as np


class IsolationForestDetector:
    def __init__(
        self,
        contamination: float = 0.1,
        random_state: int = 42,
        n_estimators: int = 100,
    ):
        self.contamination = contamination
        self.random_state = random_state
        self.n_estimators = n_estimators
        self.model = None
        self.is_fitted = False

    def _get_model(self):
        try:
            from sklearn.ensemble import IsolationForest

            return IsolationForest(
                contamination=self.contamination,
                random_state=self.random_state,
                n_estimators=self.n_estimators,
            )
        except ImportError:
            return None

    def fit(self, X: pd.DataFrame):
        self.model = self._get_model()

        if self.model is None:
            self.is_fitted = False
            return self

        try:
            self.model.fit(X)
            self.is_fitted = True
        except Exception as e:
            self.is_fitted = False

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.model is None:
            return np.zeros(len(X))

        try:
            predictions = self.model.predict(X)
            return np.where(predictions == -1, 1, 0)
        except:
            return np.zeros(len(X))

    def score_samples(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.model is None:
            return np.zeros(len(X))

        try:
            return self.model.decision_function(X)
        except:
            return np.zeros(len(X))

    def get_anomaly_scores(self, X: pd.DataFrame) -> pd.Series:
        scores = self.score_samples(X)
        return pd.Series(-scores, index=X.index)

    def detect(self, X: pd.DataFrame) -> pd.Series:
        predictions = self.predict(X)
        return pd.Series(predictions, index=X.index)

    def fit_detect(self, X: pd.DataFrame) -> pd.Series:
        self.fit(X)
        return self.detect(X)


if __name__ == "__main__":
    detector = IsolationForestDetector()
    print("Isolation Forest detector ready")
