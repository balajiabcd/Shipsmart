import os
import logging
from typing import Dict, List, Optional
import joblib
import pandas as pd

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


class PredictionIntegrator:
    def __init__(self, ml_model=None, llm_router=None, shap_explainer=None):
        self.ml_model = ml_model
        self.llm = llm_router
        self.shap = shap_explainer
        self._load_models()

    def _load_models(self):
        """Load ML model if not provided"""
        if self.ml_model is None:
            try:
                model_files = [
                    f
                    for f in os.listdir(MODEL_DIR)
                    if f.endswith(".joblib") and "classifier" in f
                ]
                if model_files:
                    model_path = os.path.join(MODEL_DIR, model_files[0])
                    self.ml_model = joblib.load(model_path)
                    logger.info(f"Loaded ML model: {model_files[0]}")
            except Exception as e:
                logger.error(f"Error loading model: {e}")

    def predict(self, delivery_context: Dict) -> Dict:
        """Get ML prediction + LLM explanation"""

        features = self._extract_features(delivery_context)

        ml_prediction = self._get_ml_prediction(features)

        top_factors = self._get_top_factors(features)

        llm_explanation = ""
        if self.llm and self.llm.is_available():
            try:
                llm_explanation = self.llm.explain_delay(
                    ml_prediction["delay_probability"], top_factors, delivery_context
                )
            except Exception as e:
                logger.error(f"LLM explanation error: {e}")

        recommendations = self._generate_recommendations(
            ml_prediction["delay_probability"], top_factors
        )

        llm_recommendations = ""
        if (
            self.llm
            and self.llm.is_available()
            and ml_prediction["delay_probability"] > 0.4
        ):
            try:
                llm_recommendations = self.llm.generate_recommendation(
                    ml_prediction["delay_probability"], delivery_context
                )
            except Exception as e:
                logger.error(f"LLM recommendation error: {e}")

        return {
            "prediction": ml_prediction,
            "explanation": llm_explanation,
            "top_factors": top_factors,
            "recommendations": recommendations,
            "llm_recommendations": llm_recommendations,
            "should_intervene": ml_prediction["delay_probability"] > 0.5,
        }

    def _extract_features(self, context: Dict) -> pd.DataFrame:
        """Extract features from delivery context"""

        feature_names = [
            "distance_km",
            "weather_severity",
            "traffic_index",
            "driver_performance",
            "warehouse_efficiency",
            "route_complexity",
            "is_holiday",
            "is_weekend",
            "hour_of_day",
            "day_of_week",
        ]

        features = {k: context.get(k, 0) for k in feature_names}

        df = pd.DataFrame([features])
        return df.fillna(0)

    def _get_ml_prediction(self, features: pd.DataFrame) -> Dict:
        """Get ML model prediction"""

        if self.ml_model is None:
            return {
                "on_time_probability": 0.7,
                "delay_probability": 0.3,
                "risk_level": "low",
            }

        try:
            proba = self.ml_model.predict_proba(features)[0]
            delay_prob = float(proba[1]) if len(proba) > 1 else 0.3

            return {
                "on_time_probability": 1 - delay_prob,
                "delay_probability": delay_prob,
                "risk_level": self._classify_risk(delay_prob),
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "on_time_probability": 0.7,
                "delay_probability": 0.3,
                "risk_level": "low",
            }

    def _get_top_factors(self, features: pd.DataFrame) -> List[Dict]:
        """Get top contributing factors"""

        feature_importance = {
            "weather_severity": "Severe weather conditions",
            "traffic_index": "High traffic congestion",
            "driver_performance": "Driver performance rating",
            "distance_km": "Delivery distance",
            "route_complexity": "Route complexity",
            "warehouse_efficiency": "Warehouse efficiency",
            "is_holiday": "Holiday affecting operations",
            "is_weekend": "Weekend delivery",
            "hour_of_day": "Time of day",
            "day_of_week": "Day of week",
        }

        values = features.iloc[0]

        factors = []
        for feat, importance in feature_importance.items():
            if feat in values.index:
                value = values[feat]
                if value != 0:
                    factors.append(
                        {
                            "feature": feat,
                            "value": float(value),
                            "description": importance,
                            "impact": "increases" if value > 0 else "decreases",
                        }
                    )

        factors.sort(key=lambda x: abs(x["value"]), reverse=True)
        return factors[:5]

    def _classify_risk(self, prob: float) -> str:
        """Classify risk level"""
        if prob > 0.7:
            return "high"
        elif prob > 0.4:
            return "medium"
        else:
            return "low"

    def _generate_recommendations(
        self, delay_prob: float, top_factors: List[Dict]
    ) -> List[str]:
        """Generate rule-based recommendations"""

        if delay_prob < 0.3:
            return ["Continue normal operations"]

        recommendations = []

        for factor in top_factors:
            feat = factor.get("feature", "")
            value = factor.get("value", 0)

            if "weather" in feat and value > 5:
                recommendations.append("Consider rerouting to avoid severe weather")
            if "traffic" in feat and value > 5:
                recommendations.append("Reschedule to off-peak hours if possible")
            if "driver" in feat and value < 0.7:
                recommendations.append("Consider assigning experienced driver")

        if not recommendations:
            recommendations.append("Monitor delivery closely")

        return recommendations[:3]

    def explain_delivery(self, delivery_id: str, context: Dict) -> Dict:
        """Get full explanation for a delivery"""

        result = self.predict(context)

        result["delivery_id"] = delivery_id
        result["context_summary"] = self._summarize_context(context)

        return result


def create_integrator(llm_router=None) -> PredictionIntegrator:
    """Factory function to create prediction integrator"""
    return PredictionIntegrator(llm_router=llm_router)
