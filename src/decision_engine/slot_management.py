import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_available_slots(location: str, date: str) -> List[Dict]:
    """Get available delivery time slots"""

    slots = [
        {
            "slot_id": f"slot_{i}",
            "date": date,
            "start_time": f"{8 + i:02d}:00",
            "end_time": f"{9 + i:02d}:00",
            "capacity": 20,
            "utilization": 0.3 * i,
            "available": True,
        }
        for i in range(1, 8)
    ]

    logger.info(f"Found {len(slots)} available slots for {date}")
    return slots


def get_weather_forecast(date: str, location: str) -> Dict:
    """Get weather forecast for a date and location (placeholder)"""
    return {
        "precipitation": 10,
        "temperature": 20,
        "wind_speed": 15,
        "conditions": "clear",
    }


def get_delivery(delivery_id: str) -> Dict:
    """Get delivery details (placeholder)"""
    return {
        "delivery_id": delivery_id,
        "scheduled_date": "2024-01-15",
        "time_slot": "10:00-11:00",
        "delivery_location": "Customer_A",
        "is_fragile": False,
    }


def calculate_slot_suitability(
    slot: Dict, delivery_context: Dict, weather: Dict = None
) -> float:
    """Score a delivery slot"""

    if weather is None:
        weather = get_weather_forecast("", "")

    score = 100

    utilization_penalty = slot.get("utilization", 0) * 30
    score -= utilization_penalty

    try:
        hour = int(slot.get("start_time", "12:00").split(":")[0])
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            score -= 20
    except:
        pass

    if weather.get("precipitation", 0) > 50:
        score -= 25

    if weather.get("wind_speed", 0) > 40:
        score -= 15

    if delivery_context.get("is_fragile", False):
        try:
            hour = int(slot.get("start_time", "12:00").split(":")[0])
            if hour < 10:
                score -= 10
        except:
            pass

    if delivery_context.get("urgent", False):
        score += 20

    return max(0, score)


def recommend_slot_change(delivery_id: str, prediction_context: Dict) -> Dict:
    """Recommend new delivery slot"""

    delivery = get_delivery(delivery_id)
    current_date = delivery.get("scheduled_date", "2024-01-15")

    available_slots = get_available_slots(
        delivery.get("delivery_location", ""), current_date
    )

    weather = get_weather_forecast(current_date, delivery.get("delivery_location", ""))

    scored_slots = [
        {**slot, "score": calculate_slot_suitability(slot, delivery, weather)}
        for slot in available_slots
    ]

    sorted_slots = sorted(scored_slots, key=lambda x: x["score"], reverse=True)
    best_slot = sorted_slots[0] if sorted_slots else None

    current_score = calculate_slot_suitability(
        {"start_time": delivery.get("time_slot", "10:00").split("-")[0].strip()},
        delivery,
        weather,
    )

    should_change = best_slot and best_slot["score"] > current_score + 10

    return {
        "delivery_id": delivery_id,
        "current_slot": delivery.get("time_slot"),
        "current_score": current_score,
        "recommended_slot": best_slot.get("slot_id") if best_slot else None,
        "recommended_time": f"{best_slot.get('start_time')}-{best_slot.get('end_time')}"
        if best_slot
        else None,
        "score": best_slot.get("score") if best_slot else None,
        "should_reschedule": should_change,
        "reason": "Lower traffic and better weather conditions",
        "alternative_slots": sorted_slots[:3],
    }


def find_next_available_slot(location: str, preferred_date: str = None) -> Dict:
    """Find next available slot"""

    if preferred_date is None:
        preferred_date = datetime.now().strftime("%Y-%m-%d")

    slots = get_available_slots(location, preferred_date)
    available = [s for s in slots if s.get("available", True)]

    return available[0] if available else None


def calculate_reschedule_cost(
    original_slot: Dict, new_slot: Dict, customer_tier: str = "standard"
) -> Dict:
    """Calculate cost of rescheduling"""

    base_cost = 0

    if customer_tier == "premium":
        base_cost = 0
    elif customer_tier == "standard":
        base_cost = 5.0
    else:
        base_cost = 10.0

    try:
        orig_hour = int(original_slot.get("start_time", "12:00").split(":")[0])
        new_hour = int(new_slot.get("start_time", "12:00").split(":")[0])
        days_diff = abs(orig_hour - new_hour) * 0.5
    except:
        days_diff = 0

    total_cost = base_cost + days_diff

    return {
        "base_cost": base_cost,
        "time_difference_cost": days_diff,
        "total_cost": total_cost,
        "customer_tier": customer_tier,
    }
