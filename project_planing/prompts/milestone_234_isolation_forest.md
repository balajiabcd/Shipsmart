# Milestone #234: Implement Isolation Forest

**Your Role:** AI/LLM Engineer

ML-based anomaly detection:

```python
# src/anomaly/isolation_forest.py

from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

class IsolationForestDetector:
    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame):
        self.model.fit(X)
        self.is_fitted = True
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        predictions = self.model.predict(X)
        return np.where(predictions == -1, 1, 0)  # 1 = anomaly, 0 = normal
    
    def score_samples(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.decision_function(X)
    
    def get_anomaly_scores(self, X: pd.DataFrame) -> pd.Series:
        scores = self.score_samples(X)
        return pd.Series(-scores, index=X.index)  # Higher = more anomalous
    
    def detect(self, X: pd.DataFrame) -> pd.Series:
        predictions = self.predict(X)
        return pd.Series(predictions, index=X.index)
```

Usage:
```python
detector = IsolationForestDetector(contamination=0.05)
detector.fit(X_train)
anomalies = detector.detect(X_test)
scores = detector.get_anomaly_scores(X_test)
```

Commit.