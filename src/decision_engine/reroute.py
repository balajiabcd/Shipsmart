import os
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_alternative_routes(
    origin: str, destination: str, current_route: Dict
) -> List[Dict]:
    """Find alternative routes for a delivery"""

    alternatives = [
        {
            "route_id": f"alt_{i}",
            "origin": origin,
            "destination": destination,
            "distance_km": current_route.get("distance_km", 0) * (1 + 0.1 * i),
            "estimated_time_min": current_route.get("estimated_time_min", 0)
            * (1 + 0.15 * i),
            "traffic_level": ["low", "medium", "high"][i % 3],
            "weather_risk": ["low", "medium", "high"][(i + 1) % 3],
            "savings_score": 10 - i * 2,
            "route_type": ["fastest", "scenic", "highway"][i % 3],
        }
        for i in range(1, 4)
    ]

    logger.info(f"Found {len(alternatives)} alternative routes")
    return sorted(alternatives, key=lambda x: x["savings_score"], reverse=True)


def evaluate_route_suitability(route: Dict, delivery_context: Dict) -> float:
    """Score a route based on delivery context"""

    score = 100

    traffic_penalty = {"low": 0, "medium": 10, "high": 20}
    score -= traffic_penalty.get(route.get("traffic_level", "low"), 0)

    weather_penalty = {"low": 0, "medium": 10, "high": 25}
    score -= weather_penalty.get(route.get("weather_risk", "low"), 0)

    if (
        delivery_context.get("is_fragile", False)
        and route.get("weather_risk") == "high"
    ):
        score -= 30

    if delivery_context.get("urgent", False):
        score -= weather_penalty.get(route.get("weather_risk", "low"), 0) * 2

    if route.get("distance_km", 0) > delivery_context.get("max_distance_km", 200):
        score -= 20

    return max(0, score)


def get_route(delivery_id: str) -> Dict:
    """Get current route for a delivery (placeholder)"""

    return {
        "delivery_id": delivery_id,
        "origin": "Warehouse_A",
        "destination": "Customer_Location",
        "distance_km": 50.0,
        "estimated_time_min": 60,
        "traffic_level": "medium",
        "weather_risk": "low",
    }


def recommend_reroute(delivery_id: str, prediction_context: Dict) -> Dict:
    """Recommend reroute if delay predicted"""

    current_route = get_route(delivery_id)

    alternatives = find_alternative_routes(
        current_route["origin"], current_route["destination"], current_route
    )

    scored_alternatives = [
        {**route, "score": evaluate_route_suitability(route, prediction_context)}
        for route in alternatives
    ]

    sorted_alternatives = sorted(
        scored_alternatives, key=lambda x: x["score"], reverse=True
    )

    return {
        "delivery_id": delivery_id,
        "current_route": current_route,
        "recommendations": sorted_alternatives,
        "should_reroute": sorted_alternatives[0]["score"] > 70
        if sorted_alternatives
        else False,
        "best_alternative": sorted_alternatives[0] if sorted_alternatives else None,
    }


def calculate_reroute_savings(current_route: Dict, alternative_route: Dict) -> Dict:
    """Calculate time and distance savings"""

    distance_saved = current_route.get("distance_km", 0) - alternative_route.get(
        "distance_km", 0
    )
    time_saved = current_route.get("estimated_time_min", 0) - alternative_route.get(
        "estimated_time_min", 0
    )

    return {
        "distance_saved_km": max(0, distance_saved),
        "time_saved_min": max(0, time_saved),
        "alternative_is_faster": time_saved > 0,
        "alternative_is_shorter": distance_saved > 0,
    }


def filter_routes_by_constraints(
    alternatives: List[Dict], constraints: Dict
) -> List[Dict]:
    """Filter alternatives by delivery constraints"""

    filtered = []

    for route in alternatives:
        if constraints.get("max_distance_km"):
            if route.get("distance_km", 0) > constraints["max_distance_km"]:
                continue

        if constraints.get("max_time_min"):
            if route.get("estimated_time_min", 0) > constraints["max_time_min"]:
                continue

        if constraints.get("avoid_highway"):
            if route.get("route_type") == "highway":
                continue

        filtered.append(route)

    logger.info(f"Filtered {len(alternatives)} routes to {len(filtered)} valid routes")
    return filtered
