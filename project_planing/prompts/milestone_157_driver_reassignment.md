# Milestone #157: Build Driver Reassignment

**Your Role:** AI/LLM Engineer

Create driver reassignment recommendation:

```python
# decision_engine/driver_assignment.py

def find_available_drivers(location: str, vehicle_type: str = None) -> list:
    """Find available drivers near a location"""
    
    # Query active drivers
    drivers = db.query("""
        SELECT driver_id, name, performance_score, vehicle_type, 
               current_location, is_available
        FROM drivers
        WHERE is_available = true 
        AND distance(current_location, ?) < 20
        ORDER BY performance_score DESC
        LIMIT 10
    """, [location])
    
    return drivers

def calculate_driver_score(driver: dict, delivery_context: dict) -> float:
    """Calculate suitability score for a driver"""
    
    score = driver["performance_score"] * 40
    
    if driver["vehicle_type"] == delivery_context["required_vehicle"]:
        score += 30
    
    if driver["experience_years"] >= delivery_context.get("experience_needed", 0):
        score += 20
    
    route_familiarity = get_route_familiarity(driver["driver_id"], delivery_context["route_id"])
    score += route_familiarity * 10
    
    return min(100, score)

def recommend_driver_reassignment(delivery_id: str, prediction_context: dict) -> dict:
    """Recommend alternative driver if delay predicted"""
    
    delivery = get_delivery(delivery_id)
    available_drivers = find_available_drivers(
        delivery["pickup_location"],
        delivery["vehicle_type"]
    )
    
    scored_drivers = [
        {
            **driver,
            "suitability_score": calculate_driver_score(driver, delivery)
        }
        for driver in available_drivers
    ]
    
    best_driver = max(scored_drivers, key=lambda x: x["suitability_score"])
    
    return {
        "delivery_id": delivery_id,
        "current_driver": delivery["driver_id"],
        "recommended_driver": best_driver["driver_id"],
        "score": best_driver["suitability_score"],
        "reason": "Higher performance and route familiarity"
    }
```

Commit.