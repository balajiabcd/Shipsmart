# Milestone #217: Add Confidence Scoring

**Your Role:** AI/LLM Engineer

Show reliability of explanations:

```python
# src/root_cause/confidence.py

import numpy as np

class ConfidenceScorer:
    def __init__(self):
        self.model = None
    
    def calculate_confidence(self, prediction: float, shap_values: list, feature_values: dict) -> dict:
        prediction_conf = self._prediction_confidence(prediction)
        shap_conf = self._shap_confidence(shap_values)
        data_conf = self._data_confidence(feature_values)
        
        overall = (prediction_conf * 0.4 + shap_conf * 0.3 + data_conf * 0.3)
        
        return {
            "overall": overall,
            "prediction_confidence": prediction_conf,
            "shap_confidence": shap_conf,
            "data_confidence": data_conf,
            "rating": self._get_rating(overall),
            "factors_considered": len(shap_values)
        }
    
    def _prediction_confidence(self, prob: float) -> float:
        distance_from_middle = abs(prob - 0.5) * 2
        return min(1.0, distance_from_middle + 0.3)
    
    def _shap_confidence(self, shap_values: list) -> float:
        if not shap_values:
            return 0.0
        
        abs_values = [abs(s["shap_value"]) for s in shap_values]
        concentration = max(abs_values) / (sum(abs_values) + 1e-6)
        
        return min(1.0, concentration * 2)
    
    def _data_quality_confidence(self, feature_values: dict) -> float:
        missing = sum(1 for v in feature_values.values() if v is None)
        total = len(feature_values)
        return 1 - (missing / total) if total > 0 else 0
    
    def _get_rating(self, score: float) -> str:
        if score >= 0.8: return "very_high"
        if score >= 0.6: return "high"
        if score >= 0.4: return "medium"
        if score >= 0.2: return "low"
        return "very_low"
```

Commit.