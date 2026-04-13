# Milestone #160: Create Recommendation Scoring

**Your Role:** AI/LLM Engineer

Create scoring system for ranking actions:

```python
# decision_engine/scoring.py

import numpy as np

def calculate_action_impact(action: dict, delivery_context: dict) -> float:
    """Calculate expected impact of an action"""
    
    base_scores = {
        "reroute": 40,
        "driver_reassignment": 35,
        "delivery_slot_change": 30,
        "customer_notification": 25
    }
    
    score = base_scores.get(action["action_type"], 10)
    
    if action["action_type"] == "reroute":
        score += (1 - action["route_risk"]) * 30
    
    if action["action_type"] == "driver_reassignment":
        score += (action["new_driver_score"] - action["old_driver_score"]) * 0.5
    
    if action["action_type"] == "delivery_slot_change":
        if action["traffic_improvement"] > 0.3:
            score += 20
    
    delay_risk = delivery_context.get("delay_probability", 0.5)
    score *= (1 + delay_risk)
    
    return min(100, score)

def rank_recommendations(recommendations: list, delivery_context: dict) -> list:
    """Rank recommendations by expected impact"""
    
    scored_recs = []
    for rec in recommendations:
        impact_score = calculate_action_impact(rec, delivery_context)
        cost = calculate_action_cost(rec["action_type"])
        
        scored_recs.append({
            **rec,
            "impact_score": impact_score,
            "cost": cost,
            "roi_score": impact_score / max(cost, 1)
        })
    
    return sorted(scored_recs, key=lambda x: x["roi_score"], reverse=True)

def calculate_action_cost(action_type: str) -> float:
    """Estimate operational cost of action"""
    
    costs = {
        "reroute": 15.0,
        "driver_reassignment": 25.0,
        "delivery_slot_change": 5.0,
        "customer_notification": 2.0
    }
    return costs.get(action_type, 10.0)
```

Commit.