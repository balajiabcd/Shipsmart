import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_cost_benefit(action: Dict, delivery_context: Dict) -> Dict:
    """Calculate cost and benefit for a recommendation"""

    action_costs = {
        "reroute": {"operational": 15, "fuel": 10, "time": 20},
        "driver_reassignment": {"operational": 25, "training": 5, "time": 15},
        "delivery_slot_change": {"operational": 5, "customer_impact": 10},
        "customer_notification": {"operational": 2, "reputation": 5},
    }

    costs = action_costs.get(action.get("action_type", "unknown"), {"operational": 10})
    total_cost = sum(costs.values())

    delay_prob = delivery_context.get("delay_probability", 0.5)
    action_effectiveness = action.get("effectiveness", 0.6)

    avoided_delay_mins = (delay_prob - (1 - action_effectiveness)) * 60

    customer_satisfaction_gain = avoided_delay_mins / 10

    penalty_per_delay = 50
    avoided_penalty = delay_prob * action_effectiveness * penalty_per_delay

    benefit = avoided_penalty + customer_satisfaction_gain * 10

    net_value = benefit - total_cost
    roi_percent = ((benefit - total_cost) / total_cost * 100) if total_cost > 0 else 0

    return {
        "action_type": action.get("action_type", "unknown"),
        "cost_breakdown": costs,
        "total_cost": total_cost,
        "estimated_benefit": benefit,
        "net_value": net_value,
        "roi_percent": roi_percent,
        "avoided_delay_mins": avoided_delay_mins,
    }


def recommend_actions_with_cba(
    recommendations: List[Dict], delivery_context: Dict
) -> List[Dict]:
    """Add cost-benefit analysis to recommendations"""

    analyzed = []
    for rec in recommendations:
        cba = calculate_cost_benefit(rec, delivery_context)
        analyzed.append({**rec, **cba})

    sorted_recs = sorted(analyzed, key=lambda x: x.get("net_value", 0), reverse=True)

    logger.info(f"Analyzed {len(sorted_recs)} recommendations with CBA")
    return sorted_recs


def calculate_total_roi(actions: List[Dict]) -> Dict:
    """Calculate total ROI for multiple actions"""

    total_cost = sum(a.get("total_cost", 0) for a in actions)
    total_benefit = sum(a.get("estimated_benefit", 0) for a in actions)
    total_net_value = sum(a.get("net_value", 0) for a in actions)

    overall_roi = (
        ((total_benefit - total_cost) / total_cost * 100) if total_cost > 0 else 0
    )

    return {
        "total_cost": total_cost,
        "total_benefit": total_benefit,
        "total_net_value": total_net_value,
        "overall_roi_percent": overall_roi,
        "number_of_actions": len(actions),
    }


def get_optimal_budget_allocation(
    available_budget: float, recommendations: List[Dict]
) -> Dict:
    """Optimize budget allocation across recommendations"""

    analyzed = recommend_actions_with_cba(recommendations, {})

    selected = []
    remaining_budget = available_budget

    for rec in analyzed:
        cost = rec.get("total_cost", 0)

        if cost <= remaining_budget:
            selected.append(rec)
            remaining_budget -= cost

    roi = calculate_total_roi(selected)

    return {
        "selected_actions": selected,
        "allocated_budget": available_budget - remaining_budget,
        "remaining_budget": remaining_budget,
        "total_roi": roi,
    }


def estimate_delivery_value(delivery_context: Dict) -> float:
    """Estimate the business value of a delivery"""

    base_value = 100

    customer_tier_multiplier = {"premium": 2.0, "standard": 1.0, "basic": 0.5}

    multiplier = customer_tier_multiplier.get(
        delivery_context.get("customer_tier", "standard"), 1.0
    )

    if delivery_context.get("is_fragile"):
        base_value *= 1.2

    if delivery_context.get("urgent"):
        base_value *= 1.5

    return base_value * multiplier


def calculate_breakeven_point(
    action_cost: float, delay_probability: float, penalty_per_delay: float = 50
) -> float:
    """Calculate required effectiveness to break even"""

    if delay_probability == 0:
        return 0

    breakeven_effectiveness = (
        action_cost / (delay_probability * penalty_per_delay)
    ) * 100

    return min(100, breakeven_effectiveness)
