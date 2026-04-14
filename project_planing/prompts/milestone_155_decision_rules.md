# Milestone #155: Design Decision Rules

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
Define rule-based logic for the decision engine:

```python
# decision_engine/rules.py

DELAY_THRESHOLD = 0.7  # High risk threshold
MEDIUM_THRESHOLD = 0.4  # Medium risk threshold

RULES = {
    "reroute": {
        "condition": "delay_probability > 0.6 AND weather_severity > 3",
        "action": "suggest_alternative_route",
        "priority": "high"
    },
    "driver_reassignment": {
        "condition": "driver_performance < 0.7 AND delay_probability > 0.5",
        "action": "reassign_to_better_driver",
        "priority": "medium"
    },
    "delivery_slot_change": {
        "condition": "traffic_index > 7 AND delay_probability > 0.4",
        "action": "reschedule_to_off_peak",
        "priority": "medium"
    },
    "customer_notification": {
        "condition": "delay_probability > 0.5",
        "action": "send_proactive_message",
        "priority": "high"
    }
}

def evaluate_rules(prediction_context: dict) -> list:
    """Evaluate all rules against prediction context"""
    triggered_rules = []
    
    for rule_name, rule_config in RULES.items():
        if evaluate_condition(rule_config["condition"], prediction_context):
            triggered_rules.append({
                "rule": rule_name,
                "action": rule_config["action"],
                "priority": rule_config["priority"]
            })
    
    return triggered_rules
```

**Completed:**
- Created `src/decision_engine/rules.py` with:
  - `RULES` - Decision rules dictionary
  - `evaluate_condition()` - Parse and evaluate conditions
  - `evaluate_rules()` - Evaluate all rules against context
  - `get_rule_by_priority()` - Filter by priority
  - `add_rule()` / `remove_rule()` - Dynamic rule management
  - `validate_rules()` - Validate rule syntax

**Next Milestone:** Proceed to #156 - Reroute Recommendation

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #156: Implement Reroute Recommendation
- Create reroute suggestion logic
- Integrate with routing service