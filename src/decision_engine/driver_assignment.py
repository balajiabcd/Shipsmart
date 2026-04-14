import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_available_drivers(location: str, vehicle_type: str = None) -> List[Dict]:
    """Find available drivers near a location"""

    mock_drivers = [
        {
            "driver_id": f"driver_{i}",
            "name": f"Driver {i}",
            "performance_score": 0.7 + (i * 0.03),
            "vehicle_type": ["van", "truck", "bike"][i % 3],
            "current_location": location,
            "is_available": True,
            "experience_years": 1 + i,
            "on_time_rate": 0.8 + (i * 0.02),
        }
        for i in range(1, 6)
    ]

    if vehicle_type:
        mock_drivers = [d for d in mock_drivers if d["vehicle_type"] == vehicle_type]

    logger.info(f"Found {len(mock_drivers)} available drivers")
    return sorted(mock_drivers, key=lambda x: x["performance_score"], reverse=True)


def get_route_familiarity(driver_id: str, route_id: str) -> float:
    """Get driver's familiarity with a route (0-1 scale)"""
    return 0.5


def get_delivery(delivery_id: str) -> Dict:
    """Get delivery details (placeholder)"""
    return {
        "delivery_id": delivery_id,
        "driver_id": "driver_1",
        "pickup_location": "Warehouse_A",
        "vehicle_type": "van",
        "route_id": "route_1",
        "required_vehicle": "van",
        "experience_needed": 2,
    }


def calculate_driver_score(driver: Dict, delivery_context: Dict) -> float:
    """Calculate suitability score for a driver"""

    score = driver.get("performance_score", 0.5) * 40

    if driver.get("vehicle_type") == delivery_context.get("required_vehicle"):
        score += 30

    if driver.get("experience_years", 0) >= delivery_context.get(
        "experience_needed", 0
    ):
        score += 20

    route_familiarity = get_route_familiarity(
        driver.get("driver_id", ""), delivery_context.get("route_id", "")
    )
    score += route_familiarity * 10

    if driver.get("on_time_rate", 0) > 0.9:
        score += 10

    return min(100, score)


def recommend_driver_reassignment(delivery_id: str, prediction_context: Dict) -> Dict:
    """Recommend alternative driver if delay predicted"""

    delivery = get_delivery(delivery_id)
    available_drivers = find_available_drivers(
        delivery["pickup_location"], delivery.get("vehicle_type")
    )

    scored_drivers = [
        {**driver, "suitability_score": calculate_driver_score(driver, delivery)}
        for driver in available_drivers
    ]

    sorted_drivers = sorted(
        scored_drivers, key=lambda x: x["suitability_score"], reverse=True
    )
    best_driver = sorted_drivers[0] if sorted_drivers else None

    current_driver_score = delivery.get("driver_performance", 0.7)
    should_reassign = (
        best_driver
        and best_driver["suitability_score"] > current_driver_score * 100 + 10
    )

    return {
        "delivery_id": delivery_id,
        "current_driver": delivery["driver_id"],
        "current_driver_score": current_driver_score,
        "recommended_driver": best_driver["driver_id"] if best_driver else None,
        "score": best_driver["suitability_score"] if best_driver else None,
        "should_reassign": should_reassign,
        "reason": "Higher performance and route familiarity",
        "alternative_drivers": sorted_drivers[:3],
    }


def filter_drivers_by_availability(
    drivers: List[Dict], required_vehicle: str = None, min_performance: float = 0.5
) -> List[Dict]:
    """Filter drivers by availability and requirements"""

    filtered = []

    for driver in drivers:
        if not driver.get("is_available", False):
            continue

        if required_vehicle and driver.get("vehicle_type") != required_vehicle:
            continue

        if driver.get("performance_score", 0) < min_performance:
            continue

        filtered.append(driver)

    logger.info(f"Filtered {len(drivers)} to {len(filtered)} valid drivers")
    return filtered


def calculate_reassignment_cost(
    current_driver: Dict, new_driver: Dict, distance_km: float
) -> Dict:
    """Calculate cost of reassigning driver"""

    base_cost = 25.0
    distance_cost = distance_km * 0.5

    driver_change_cost = 15.0

    total_cost = base_cost + distance_cost + driver_change_cost

    return {
        "base_cost": base_cost,
        "distance_cost": distance_cost,
        "driver_change_cost": driver_change_cost,
        "total_cost": total_cost,
    }
