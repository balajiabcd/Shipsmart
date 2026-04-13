# Milestone #163: Build Cost-Benefit Analysis

**Your Role:** AI/LLM Engineer

Calculate cost-benefit for each action:

```python
# decision_engine/cost_benefit.py

def calculate_cost_benefit(action: dict, delivery_context: dict) -> dict:
    """Calculate cost and benefit for a recommendation"""
    
    action_costs = {
        "reroute": {"operational": 15, "fuel": 10, "time": 20},
        "driver_reassignment": {"operational": 25, "training": 5, "time": 15},
        "delivery_slot_change": {"operational": 5, "customer_impact": 10},
        "customer_notification": {"operational": 2, "reputation": 5}
    }
    
    costs = action_costs.get(action["action_type"], {"operational": 10})
    total_cost = sum(costs.values())
    
    delay_prob = delivery_context.get("delay_probability", 0.5)
    action_effectiveness = action.get("effectiveness", 0.6)
    
    avoided_delay_mins = (delay_prob - (1 - action_effectiveness)) * 60
    customer_satisfaction_gain = avoided_delay_mins / 10
    
    penalty_per_delay = 50  # Customer refund/compensation
    avoided_penalty = delay_prob * action_effectiveness * penalty_per_delay
    
    benefit = avoided_penalty + customer_satisfaction_gain * 10
    
    return {
        "action_type": action["action_type"],
        "total_cost": total_cost,
        "estimated_benefit": benefit,
        "net_value": benefit - total_cost,
        "roi_percent": ((benefit - total_cost) / total_cost * 100) if total_cost > 0 else 0
    }

def recommend_actions_with_cba(recommendations: list, delivery_context: dict) -> list:
    """Add cost-benefit analysis to recommendations"""
    
    analyzed = []
    for rec in recommendations:
        cba = calculate_cost_benefit(rec, delivery_context)
        analyzed.append({**rec, **cba})
    
    return sorted(analyzed, key=lambda x: x["net_value"], reverse=True)
```

Commit.