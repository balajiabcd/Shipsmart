import numpy as np
from typing import Dict, List


class ConfidenceScorer:
    def __init__(self):
        self.model = None

    def set_model(self, model):
        self.model = model

    def calculate_confidence(
        self, prediction: float, shap_values: list, feature_values: dict
    ) -> dict:
        prediction_conf = self._prediction_confidence(prediction)
        shap_conf = self._shap_confidence(shap_values)
        data_conf = self._data_confidence(feature_values)

        overall = prediction_conf * 0.4 + shap_conf * 0.3 + data_conf * 0.3

        return {
            "overall": round(overall, 3),
            "prediction_confidence": round(prediction_conf, 3),
            "shap_confidence": round(shap_conf, 3),
            "data_confidence": round(data_conf, 3),
            "rating": self._get_rating(overall),
            "factors_considered": len(shap_values),
        }

    def _prediction_confidence(self, prob: float) -> float:
        distance_from_middle = abs(prob - 0.5) * 2
        return min(1.0, distance_from_middle + 0.3)

    def _shap_confidence(self, shap_values: list) -> float:
        if not shap_values:
            return 0.0

        abs_values = [abs(s.get("shap_value", 0)) for s in shap_values]
        if not abs_values or sum(abs_values) == 0:
            return 0.5

        concentration = max(abs_values) / (sum(abs_values) + 1e-6)

        return min(1.0, concentration * 2)

    def _data_confidence(self, feature_values: dict) -> float:
        if not feature_values:
            return 0.5

        missing = sum(1 for v in feature_values.values() if v is None or v == "unknown")
        total = len(feature_values)

        if total == 0:
            return 0.5

        return 1 - (missing / total)

    def _get_rating(self, score: float) -> str:
        if score >= 0.8:
            return "very_high"
        if score >= 0.6:
            return "high"
        if score >= 0.4:
            return "medium"
        if score >= 0.2:
            return "low"
        return "very_low"

    def get_confidence_level(self, rating: str) -> Dict:
        levels = {
            "very_high": {
                "color": "green",
                "icon": "✓✓",
                "description": "Highly reliable",
            },
            "high": {"color": "lightgreen", "icon": "✓", "description": "Reliable"},
            "medium": {
                "color": "yellow",
                "icon": "○",
                "description": "Moderate reliability",
            },
            "low": {"color": "orange", "icon": "!", "description": "Low reliability"},
            "very_low": {"color": "red", "icon": "✗", "description": "Unreliable"},
        }
        return levels.get(rating, levels["medium"])


if __name__ == "__main__":
    scorer = ConfidenceScorer()
    result = scorer.calculate_confidence(
        prediction=0.78,
        shap_values=[
            {"feature": "weather", "shap_value": 0.45},
            {"feature": "traffic", "shap_value": 0.32},
        ],
        feature_values={"weather": "rain", "traffic": "high"},
    )
    print(f"Confidence: {result}")
