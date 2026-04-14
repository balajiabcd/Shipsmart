# Milestone #158: Build Delivery Slot Change

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
Create delivery slot rescheduling recommendation:

```python
# decision_engine/slot_management.py

def get_available_slots(location: str, date: str) -> list:
    """Get available delivery time slots"""
    
    slots = [
        {"slot_id": f"slot_{i}", "start_time": f"0{8+i}:00", "end_time": f"0{9+i}:00", "capacity": 20, "utilization": 0.3 * i}
        for i in range(1, 8)
    ]
    
    return slots

def calculate_slot_suitability(slot: dict, delivery_context: dict, weather: dict) -> float:
    """Score a delivery slot"""
    
    score = 100
    
    utilization_penalty = slot["utilization"] * 30
    score -= utilization_penalty
    
    hour = int(slot["start_time"].split(":")[0])
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        score -= 20  # Rush hour penalty
    
    if weather["precipitation"] > 50:
        score -= 25
    
    if delivery_context["is_fragile"]:
        if hour < 10:
            score -= 10  # Too early for fragile items
    
    return max(0, score)

def recommend_slot_change(delivery_id: str, prediction_context: dict) -> dict:
    """Recommend new delivery slot"""
    
    delivery = get_delivery(delivery_id)
    current_date = delivery["scheduled_date"]
    
    available_slots = get_available_slots(delivery["delivery_location"], current_date)
    
    weather = get_weather_forecast(current_date, delivery["delivery_location"])
    
    scored_slots = [
        {**slot, "score": calculate_slot_suitability(slot, delivery, weather)}
        for slot in available_slots
    ]
    
    best_slot = max(scored_slots, key=lambda x: x["score"])
    
    return {
        "delivery_id": delivery_id,
        "current_slot": delivery["time_slot"],
        "recommended_slot": best_slot["slot_id"],
        "score": best_slot["score"],
        "reason": "Lower traffic and better weather conditions"
    }
```

**Completed:**
- Created `src/decision_engine/slot_management.py` with:
  - `get_available_slots()` - Get available time slots
  - `calculate_slot_suitability()` - Score slot suitability
  - `recommend_slot_change()` - Get slot change recommendation
  - `find_next_available_slot()` - Find next slot
  - `calculate_reschedule_cost()` - Cost calculation

**Next Milestone:** Proceed to #159 - Customer Notification

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #159: Implement Customer Notification Logic
- Create notification templates
- Handle proactive messaging