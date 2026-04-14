import os
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_action_impact(action: Dict, delivery_context: Dict) -> float:
    """Calculate expected impact of an action"""

    base_scores = {
        "reroute": 40,
        "driver_reassignment": 35,
        "delivery_slot_change": 30,
        "customer_notification": 25,
    }

    score = base_scores.get(action.get("action_type", "unknown"), 10)

    if action.get("action_type") == "reroute":
        route_risk = action.get("route_risk", 0.5)
        score += (1 - route_risk) * 30

    if action.get("action_type") == "driver_reassignment":
        new_score = action.get("new_driver_score", 0.7)
        old_score = action.get("old_driver_score", 0.7)
        score += (new_score - old_score) * 50

    if action.get("action_type") == "delivery_slot_change":
        traffic_improvement = action.get("traffic_improvement", 0)
        if traffic_improvement > 0.3:
            score += 20

    if action.get("action_type") == "customer_notification":
        urgency = action.get("urgency", "low")
        urgency_multiplier = {"high": 1.5, "medium": 1.2, "low": 1.0}
        score *= urgency_multiplier.get(urgency, 1.0)

    delay_risk = delivery_context.get("delay_probability", 0.5)
    score *= 1 + delay_risk

    return min(100, max(0, score))


def calculate_action_cost(action_type: str) -> float:
    """Estimate operational cost of action"""

    costs = {
        "reroute": 15.0,
        "driver_reassignment": 25.0,
        "delivery_slot_change": 5.0,
        "customer_notification": 2.0,
    }
    return costs.get(action_type, 10.0)


def rank_recommendations(
    recommendations: List[Dict], delivery_context: Dict
) -> List[Dict]:
    """Rank recommendations by expected impact"""

    scored_recs = []

    for rec in recommendations:
        impact_score = calculate_action_impact(rec, delivery_context)
        cost = calculate_action_cost(rec.get("action_type", "unknown"))

        scored_recs.append(
            {
                **rec,
                "impact_score": impact_score,
                "cost": cost,
                "roi_score": impact_score / max(cost, 1),
            }
        )

    sorted_recs = sorted(scored_recs, key=lambda x: x["roi_score"], reverse=True)

    logger.info(f"Ranked {len(sorted_recs)} recommendations")
    return sorted_recs


def get_top_recommendations(
    ranked_recommendations: List[Dict], n: int = 3
) -> List[Dict]:
    """Get top N recommendations"""
    return ranked_recommendations[:n]


def filter_by_budget(recommendations: List[Dict], budget: float) -> List[Dict]:
    """Filter recommendations by available budget"""

    filtered = []
    total_cost = 0

    for rec in recommendations:
        cost = calculate_action_cost(rec.get("action_type", "unknown"))

        if total_cost + cost <= budget:
            filtered.append(rec)
            total_cost += cost

    logger.info(
        f"Filtered {len(recommendations)} to {len(filtered)} within budget ${budget}"
    )
    return filtered


def calculate_total_expected_benefit(ranked_recommendations: List[Dict]) -> float:
    """Calculate total expected benefit from all recommendations"""

    total = sum(rec.get("impact_score", 0) for rec in ranked_recommendations)
    return total


def create_execution_plan(
    ranked_recommendations: List[Dict], budget: float = None
) -> Dict:
    """Create execution plan from ranked recommendations"""

    if budget:
        feasible_recs = filter_by_budget(ranked_recommendations, budget)
    else:
        feasible_recs = ranked_recommendations

    total_cost = sum(
        calculate_action_cost(r.get("action_type", "unknown")) for r in feasible_recs
    )
    total_impact = calculate_total_expected_benefit(feasible_recs)

    execution_order = [
        {
            "step": i + 1,
            "action": rec.get("action_type"),
            "description": rec.get("description", ""),
            "cost": calculate_action_cost(rec.get("action_type", "unknown")),
            "impact": rec.get("impact_score", 0),
        }
        for i, rec in enumerate(feasible_recs)
    ]

    return {
        "recommendations": execution_order,
        "total_cost": total_cost,
        "total_impact": total_impact,
        "number_of_actions": len(feasible_recs),
    }
