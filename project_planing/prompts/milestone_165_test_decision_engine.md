# Milestone #165: Test Decision Engine

**Your Role:** AI/LLM Engineer

Validate decision engine recommendations:

```python
# tests/test_decision_engine.py

import pytest
from decision_engine.hybrid_engine import HybridDecisionEngine

@pytest.fixture
def engine():
    model = load_trained_model()
    rules = load_rules_config()
    return HybridDecisionEngine(model, rules)

@pytest.fixture
def sample_context():
    return {
        "delivery_id": "DEL001",
        "origin": "Warehouse_A",
        "destination": "Customer_Location_1",
        "scheduled_time": "2024-01-15T10:00:00",
        "driver_id": "DRV001",
        "vehicle_type": "van",
        "is_fragile": False,
        "customer_tier": "premium",
        "weather_severity": 3,
        "traffic_index": 6
    }

def test_high_risk_recommendations(engine, sample_context):
    sample_context["delay_probability"] = 0.85
    result = engine.make_decision(sample_context)
    
    assert result["risk_level"] == "high"
    assert result["should_intervene"] == True
    assert len(result["recommendations"]) > 0
    assert any(r["action_type"] == "customer_notification" for r in result["recommendations"])

def test_low_risk_no_intervention(engine, sample_context):
    sample_context["delay_probability"] = 0.2
    result = engine.make_decision(sample_context)
    
    assert result["risk_level"] == "low"
    assert result["should_intervene"] == False

def test_priority_queue_ordering():
    from decision_engine.priority_queue import DeliveryPriorityQueue
    
    pq = DeliveryPriorityQueue()
    pq.enqueue("DEL001", {"delay_probability": 0.8})
    pq.enqueue("DEL002", {"delay_probability": 0.3})
    pq.enqueue("DEL003", {"delay_probability": 0.6})
    
    first = pq.dequeue()
    assert first.delivery_id == "DEL001"

def test_cost_benefit_calculation():
    from decision_engine.cost_benefit import calculate_cost_benefit
    
    action = {"action_type": "reroute", "effectiveness": 0.7}
    context = {"delay_probability": 0.6}
    
    result = calculate_cost_benefit(action, context)
    
    assert result["total_cost"] > 0
    assert result["net_value"] >= 0
    assert result["roi_percent"] >= 0
```

Run tests:
```bash
pytest tests/test_decision_engine.py -v
```

Commit tests.