# Milestone #242: Test Anomaly Detection

**Your Role:** AI/LLM Engineer

Validate detection accuracy:

```python
# tests/test_anomaly_detection.py

import pytest
import numpy as np
import pandas as pd
from src.anomaly.statistical_detection import StatisticalAnomalyDetector
from src.anomaly.isolation_forest import IsolationForestDetector

@pytest.fixture
def sample_data():
    np.random.seed(42)
    normal = np.random.normal(50, 5, 100)
    anomalies = np.array([100, 110, 95])
    return np.concatenate([normal, anomalies])

def test_statistical_detector(sample_data):
    detector = StatisticalAnomalyDetector(z_threshold=2.5)
    series = pd.Series(sample_data)
    
    detector.fit(series[:100])
    is_anomaly = detector.detect(series)
    
    assert sum(is_anomaly) >= 2  # Should detect at least 2 of 3 anomalies

def test_isolation_forest():
    X = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100)
    })
    
    detector = IsolationForestDetector(contamination=0.1)
    detector.fit(X)
    predictions = detector.detect(X)
    
    assert sum(predictions) <= 15  # At most 10% as anomalies

def test_severity_classification():
    from src.anomaly.severity import SeverityClassifier
    
    classifier = SeverityClassifier()
    
    alert = {"metric": "driver_count", "value": 2}
    severity = classifier.classify(alert)
    
    assert severity in ["critical", "high", "medium", "low"]
```

Run: `pytest tests/test_anomaly_detection.py -v`

Commit.