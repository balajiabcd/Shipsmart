import pytest
from src.decision_engine.hybrid_engine import HybridDecisionEngine
from src.decision_engine.priority_queue import DeliveryPriorityQueue, QueueItem
from src.decision_engine.cost_benefit import (
    calculate_cost_benefit,
    recommend_actions_with_cba,
)
from src.decision_engine.rules import evaluate_rules, RULES
from src.decision_engine.scoring import rank_recommendations, calculate_action_impact
from src.decision_engine.reroute import recommend_reroute, evaluate_route_suitability
from src.decision_engine.driver_assignment import (
    recommend_driver_reassignment,
    calculate_driver_score,
)
from src.decision_engine.slot_management import (
    recommend_slot_change,
    calculate_slot_suitability,
)
from src.decision_engine.notifications import (
    generate_delay_notification,
    should_send_notification,
)


@pytest.fixture
def engine():
    return HybridDecisionEngine()


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
        "traffic_index": 6,
        "distance_km": 50,
        "driver_performance": 0.8,
    }


class TestDecisionEngine:
    def test_high_risk_detection(self, engine, sample_context):
        sample_context["delay_probability"] = 0.85
        result = engine.predict(sample_context)

        assert result["risk_level"] == "high"
        assert result["should_intervene"] == True

    def test_low_risk_no_intervention(self, engine, sample_context):
        sample_context["delay_probability"] = 0.2
        result = engine.predict(sample_context)

        assert result["risk_level"] == "low"
        assert result["should_intervene"] == False

    def test_medium_risk_detection(self, engine, sample_context):
        sample_context["delay_probability"] = 0.5
        result = engine.predict(sample_context)

        assert result["risk_level"] == "medium"


class TestPriorityQueue:
    def test_enqueue_and_dequeue(self):
        pq = DeliveryPriorityQueue()
        pq.enqueue("DEL001", {"delay_probability": 0.8})
        pq.enqueue("DEL002", {"delay_probability": 0.3})

        first = pq.dequeue()
        assert first.delivery_id == "DEL002"

    def test_priority_ordering(self):
        pq = DeliveryPriorityQueue()
        pq.enqueue("DEL001", {"delay_probability": 0.8})
        pq.enqueue("DEL002", {"delay_probability": 0.3})
        pq.enqueue("DEL003", {"delay_probability": 0.6})

        first = pq.dequeue()
        assert first.delivery_id == "DEL002"

    def test_batch_retrieval(self):
        pq = DeliveryPriorityQueue()
        for i in range(10):
            pq.enqueue(f"DEL{i:03d}", {"delay_probability": 0.5})

        batch = pq.get_next_batch(5)
        assert len(batch) == 5

    def test_get_high_risk(self):
        pq = DeliveryPriorityQueue()
        pq.enqueue("DEL001", {"delay_probability": 0.8})
        pq.enqueue("DEL002", {"delay_probability": 0.3})
        pq.enqueue("DEL003", {"delay_probability": 0.9})

        high_risk = pq.get_high_risk_deliveries(0.7)
        assert len(high_risk) == 2


class TestCostBenefit:
    def test_reroute_cost_benefit(self):
        action = {"action_type": "reroute", "effectiveness": 0.7}
        context = {"delay_probability": 0.6}

        result = calculate_cost_benefit(action, context)

        assert result["total_cost"] > 0
        assert "cost_breakdown" in result
        assert "net_value" in result

    def test_notification_cost(self):
        action = {"action_type": "customer_notification", "effectiveness": 0.8}
        context = {"delay_probability": 0.5}

        result = calculate_cost_benefit(action, context)

        assert result["total_cost"] < result["estimated_benefit"]

    def test_cba_ranking(self):
        recommendations = [
            {"action_type": "reroute", "effectiveness": 0.7},
            {"action_type": "customer_notification", "effectiveness": 0.8},
        ]
        context = {"delay_probability": 0.6}

        ranked = recommend_actions_with_cba(recommendations, context)

        assert len(ranked) == 2
        assert ranked[0]["net_value"] >= ranked[1]["net_value"]


class TestRules:
    def test_trigger_reroute_rule(self):
        context = {"delay_probability": 0.7, "weather_severity": 4}

        triggered = evaluate_rules(context, RULES)

        assert len(triggered) > 0

    def test_no_trigger_low_risk(self):
        context = {"delay_probability": 0.2, "weather_severity": 1}

        triggered = evaluate_rules(context, RULES)

        assert len(triggered) == 0


class TestScoring:
    def test_action_impact_scoring(self):
        action = {"action_type": "reroute", "route_risk": 0.3}
        context = {"delay_probability": 0.7}

        impact = calculate_action_impact(action, context)

        assert impact > 0
        assert impact <= 100

    def test_ranking_by_roi(self):
        recommendations = [
            {"action_type": "reroute", "route_risk": 0.3},
            {"action_type": "customer_notification", "urgency": "high"},
        ]
        context = {"delay_probability": 0.6}

        ranked = rank_recommendations(recommendations, context)

        assert len(ranked) == 2
        assert "roi_score" in ranked[0]


class TestReroute:
    def test_route_evaluation(self):
        route = {"traffic_level": "low", "weather_risk": "low"}
        context = {"is_fragile": False}

        score = evaluate_route_suitability(route, context)

        assert score >= 80

    def test_recommend_reroute(self):
        context = {"delay_probability": 0.8, "is_fragile": True}

        result = recommend_reroute("DEL001", context)

        assert "recommendations" in result


class TestNotifications:
    def test_generate_notification(self):
        context = {
            "delay_probability": 0.8,
            "top_factors": ["weather"],
            "expected_delay_mins": 30,
        }

        notification = generate_delay_notification("DEL001", context)

        assert "message" in notification
        assert notification["urgency"] == "high"

    def test_should_notify_premium(self):
        context = {"delay_probability": 0.35}

        should_notify = should_send_notification(context, "premium")

        assert should_notify == True

    def test_should_notify_standard(self):
        context = {"delay_probability": 0.35}

        should_notify = should_send_notification(context, "standard")

        assert should_notify == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
