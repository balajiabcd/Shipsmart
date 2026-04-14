import os
import logging
from typing import Dict, List, Optional
import joblib
import pandas as pd

from .rules import evaluate_rules, RULES
from .reroute import recommend_reroute
from .driver_assignment import recommend_driver_reassignment
from .slot_management import recommend_slot_change
from .notifications import generate_delay_notification, should_send_notification
from .scoring import rank_recommendations, create_execution_plan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


class HybridDecisionEngine:
    def __init__(self, ml_model=None, rules_config=None):
        self.ml_model = ml_model
        self.rules = rules_config or RULES
        self._load_model()

    def _load_model(self):
        if self.ml_model is None:
            model_files = [
                f
                for f in os.listdir(MODEL_DIR)
                if f.endswith(".joblib") and "classifier" in f
            ]
            if model_files:
                model_path = os.path.join(MODEL_DIR, model_files[0])
                self.ml_model = joblib.load(model_path)
                logger.info(f"Loaded model: {model_files[0]}")

    def predict(self, features: Dict) -> Dict:
        """Make prediction and generate recommendations"""

        ml_prediction = self._get_ml_prediction(features)

        features["delay_probability"] = ml_prediction.get("delay_probability", 0)

        triggered_rules = evaluate_rules(features, self.rules)

        recommendations = self._generate_recommendations(
            ml_prediction, triggered_rules, features
        )

        ranked_recommendations = rank_recommendations(recommendations, features)

        execution_plan = create_execution_plan(ranked_recommendations, budget=50.0)

        return {
            "prediction": ml_prediction,
            "risk_level": self._classify_risk(
                ml_prediction.get("delay_probability", 0)
            ),
            "triggered_rules": [r["rule"] for r in triggered_rules],
            "recommendations": ranked_recommendations,
            "execution_plan": execution_plan,
            "should_intervene": ml_prediction.get("delay_probability", 0) > 0.5
            or len(triggered_rules) > 0,
        }

    def _get_ml_prediction(self, features: Dict) -> Dict:
        """Get ML model prediction"""

        if self.ml_model is None:
            return {"delay_probability": 0.3, "on_time_probability": 0.7}

        try:
            df = pd.DataFrame([features])
            df = df.fillna(0)

            proba = self.ml_model.predict_proba(df)[0]
            delay_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

            return {
                "delay_probability": delay_prob,
                "on_time_probability": 1 - delay_prob,
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {"delay_probability": 0.3, "on_time_probability": 0.7}

    def _generate_recommendations(self, ml_pred, rules, context) -> List[Dict]:
        """Generate recommendations based on ML and rules"""

        recommendations = []

        delay_prob = ml_pred.get("delay_probability", 0)

        if delay_prob > 0.6:
            reroute_rec = self._get_reroute_recommendation(context)
            if reroute_rec:
                recommendations.append(reroute_rec)

        if delay_prob > 0.5:
            driver_rec = self._get_driver_recommendation(context)
            if driver_rec:
                recommendations.append(driver_rec)

        if delay_prob > 0.4:
            slot_rec = self._get_slot_recommendation(context)
            if slot_rec:
                recommendations.append(slot_rec)

        if should_send_notification(context):
            notif_rec = self._get_notification_recommendation(context)
            if notif_rec:
                recommendations.append(notif_rec)

        for rule in rules:
            rec = self._rule_to_recommendation(rule, context)
            if rec:
                recommendations.append(rec)

        return recommendations

    def _get_reroute_recommendation(self, context: Dict) -> Optional[Dict]:
        """Get reroute recommendation"""

        try:
            reroute_result = recommend_reroute(
                context.get("delivery_id", "unknown"), context
            )

            if reroute_result.get("should_reroute"):
                return {
                    "action_type": "reroute",
                    "description": "Suggest alternative route",
                    "route_risk": 1 - reroute_result["best_alternative"]["score"] / 100
                    if reroute_result.get("best_alternative")
                    else 0.5,
                    "data": reroute_result,
                }
        except Exception as e:
            logger.error(f"Reroute recommendation error: {e}")

        return None

    def _get_driver_recommendation(self, context: Dict) -> Optional[Dict]:
        """Get driver reassignment recommendation"""

        try:
            driver_result = recommend_driver_reassignment(
                context.get("delivery_id", "unknown"), context
            )

            if driver_result.get("should_reassign"):
                return {
                    "action_type": "driver_reassignment",
                    "description": "Reassign to better driver",
                    "new_driver_score": driver_result.get("score", 0.7) / 100,
                    "old_driver_score": driver_result.get("current_driver_score", 0.7),
                    "data": driver_result,
                }
        except Exception as e:
            logger.error(f"Driver reassignment error: {e}")

        return None

    def _get_slot_recommendation(self, context: Dict) -> Optional[Dict]:
        """Get slot change recommendation"""

        try:
            slot_result = recommend_slot_change(
                context.get("delivery_id", "unknown"), context
            )

            if slot_result.get("should_reschedule"):
                return {
                    "action_type": "delivery_slot_change",
                    "description": "Reschedule to better time slot",
                    "traffic_improvement": 0.3,
                    "data": slot_result,
                }
        except Exception as e:
            logger.error(f"Slot change error: {e}")

        return None

    def _get_notification_recommendation(self, context: Dict) -> Optional[Dict]:
        """Get notification recommendation"""

        try:
            notification = generate_delay_notification(
                context.get("delivery_id", "unknown"), context
            )

            return {
                "action_type": "customer_notification",
                "description": "Send proactive notification",
                "urgency": notification.get("urgency", "low"),
                "data": notification,
            }
        except Exception as e:
            logger.error(f"Notification error: {e}")

        return None

    def _rule_to_recommendation(self, rule: Dict, context: Dict) -> Optional[Dict]:
        """Convert triggered rule to recommendation"""

        action_map = {
            "suggest_alternative_route": "reroute",
            "reassign_to_better_driver": "driver_reassignment",
            "reschedule_to_off_peak": "delivery_slot_change",
            "send_proactive_message": "customer_notification",
        }

        action_type = action_map.get(rule.get("action"), rule.get("action"))

        return {
            "action_type": action_type,
            "description": f"Rule triggered: {rule.get('rule')}",
            "priority": rule.get("priority", "medium"),
            "rule_name": rule.get("rule"),
        }

    def _classify_risk(self, prob: float) -> str:
        """Classify risk level"""

        if prob > 0.7:
            return "high"
        elif prob > 0.4:
            return "medium"
        else:
            return "low"
