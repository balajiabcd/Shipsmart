# Milestone #156: Build Reroute Recommendation

**Your Role:** AI/LLM Engineer

Create alternative route suggestion logic:

```python
# decision_engine/reroute.py

def find_alternative_routes(origin: str, destination: str, current_route: dict) -> list:
    """Find alternative routes for a delivery"""
    
    alternatives = [
        {
            "route_id": f"alt_{i}",
            "distance_km": current_route["distance"] * (1 + 0.1 * i),
            "estimated_time_min": current_route["duration"] * (1 + 0.15 * i),
            "traffic_level": ["low", "medium", "high"][i % 3],
            "weather_risk": ["low", "medium", "high"][(i+1) % 3],
            "savings_score": 10 - i * 2
        }
        for i in range(1, 4)
    ]
    
    return sorted(alternatives, key=lambda x: x["savings_score"], reverse=True)

def evaluate_route_suitability(route: dict, delivery_context: dict) -> float:
    """Score a route based on delivery context"""
    
    score = 100
    
    if route["traffic_level"] == "high":
        score -= 20
    if route["weather_risk"] == "high":
        score -= 25
    
    if delivery_context["is_fragile"] and route["weather_risk"] == "high":
        score -= 30
    
    return max(0, score)

def recommend_reroute(delivery_id: str, prediction_context: dict) -> dict:
    """Recommend reroute if delay predicted"""
    
    current_route = get_route(delivery_id)
    alternatives = find_alternative_routes(
        current_route["origin"], 
        current_route["destination"],
        current_route
    )
    
    scored_alternatives = [
        {**route, "score": evaluate_route_suitability(route, prediction_context)}
        for route in alternatives
    ]
    
    return {
        "delivery_id": delivery_id,
        "current_route": current_route,
        "recommendations": sorted(scored_alternatives, key=lambda x: x["score"], reverse=True),
        "should_reroute": scored_alternatives[0]["score"] > 70
    }
```

Save to `src/decision_engine/reroute.py`. Commit.