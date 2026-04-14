import os
import json
import logging
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DELAY_THRESHOLD = 0.7
MEDIUM_THRESHOLD = 0.4

RULES = {
    "reroute": {
        "condition": "delay_probability > 0.6 AND weather_severity > 3",
        "action": "suggest_alternative_route",
        "priority": "high",
    },
    "driver_reassignment": {
        "condition": "driver_performance < 0.7 AND delay_probability > 0.5",
        "action": "reassign_to_better_driver",
        "priority": "medium",
    },
    "delivery_slot_change": {
        "condition": "traffic_index > 7 AND delay_probability > 0.4",
        "action": "reschedule_to_off_peak",
        "priority": "medium",
    },
    "customer_notification": {
        "condition": "delay_probability > 0.5",
        "action": "send_proactive_message",
        "priority": "high",
    },
}


def load_rules(filepath: str = None) -> Dict:
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "rules_config.json")

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)

    return RULES


def save_rules(rules: Dict, filepath: str = None):
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "rules_config.json")

    with open(filepath, "w") as f:
        json.dump(rules, f, indent=2)

    logger.info(f"Rules saved to {filepath}")


def evaluate_condition(condition: str, context: Dict) -> bool:
    try:
        context_vars = {
            "delay_probability": context.get("delay_probability", 0),
            "weather_severity": context.get("weather_severity", 0),
            "driver_performance": context.get("driver_performance", 1.0),
            "traffic_index": context.get("traffic_index", 0),
            "distance_km": context.get("distance_km", 0),
            "warehouse_efficiency": context.get("warehouse_efficiency", 1.0),
            "route_complexity": context.get("route_complexity", 0),
            "is_holiday": context.get("is_holiday", False),
            "is_weekend": context.get("is_weekend", False),
            "hour_of_day": context.get("hour_of_day", 12),
        }

        condition = condition.replace("AND", " and ").replace("OR", " or ")
        condition = condition.replace(">", " > ").replace("<", " < ")
        condition = condition.replace(">=", " >= ").replace("<=", " <= ")
        condition = condition.replace("==", " == ")

        result = eval(condition, {"__builtins__": {}}, context_vars)
        return bool(result)

    except Exception as e:
        logger.error(f"Error evaluating condition '{condition}': {e}")
        return False


def evaluate_rules(prediction_context: dict, custom_rules: Dict = None) -> List[Dict]:
    rules = custom_rules or RULES

    triggered_rules = []

    for rule_name, rule_config in rules.items():
        if evaluate_condition(rule_config["condition"], prediction_context):
            triggered_rules.append(
                {
                    "rule": rule_name,
                    "action": rule_config["action"],
                    "priority": rule_config["priority"],
                    "context": prediction_context,
                }
            )

    triggered_rules.sort(
        key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]]
    )

    logger.info(f"Triggered {len(triggered_rules)} rules")
    return triggered_rules


def get_rule_by_priority(triggered_rules: List[Dict], priority: str) -> List[Dict]:
    return [r for r in triggered_rules if r["priority"] == priority]


def add_rule(rule_name: str, condition: str, action: str, priority: str = "medium"):
    RULES[rule_name] = {"condition": condition, "action": action, "priority": priority}
    logger.info(f"Added rule: {rule_name}")
    return RULES


def remove_rule(rule_name: str) -> bool:
    if rule_name in RULES:
        del RULES[rule_name]
        logger.info(f"Removed rule: {rule_name}")
        return True
    return False


def validate_rules(rules: Dict = None) -> List[str]:
    rules = rules or RULES
    errors = []

    for rule_name, rule_config in rules.items():
        try:
            test_context = {
                "delay_probability": 0.5,
                "weather_severity": 3,
                "driver_performance": 0.8,
                "traffic_index": 5,
                "distance_km": 50,
                "warehouse_efficiency": 0.9,
                "route_complexity": 5,
                "is_holiday": False,
                "is_weekend": False,
                "hour_of_day": 10,
            }

            evaluate_condition(rule_config["condition"], test_context)

        except Exception as e:
            errors.append(f"Rule '{rule_name}': {str(e)}")

    if errors:
        logger.warning(f"Rule validation errors: {errors}")
    else:
        logger.info("All rules validated successfully")

    return errors
