import pytest
from pathlib import Path


class TestDecisionEngine:
    """Test decision engine logic (Milestone 380)"""

    def test_reroute_recommendation(self):
        """Test reroute recommendation generation"""
        from decision_engine.reroute import recommend_reroute

        context = {
            "weather_severity": 5,
            "traffic_index": 8,
            "distance_km": 100,
            "current_route": ["Berlin", "Leipzig"],
            "alternative_routes": [
                {"route": ["Berlin", "Magdeburg", "Leipzig"], "distance_km": 110},
                {"route": ["Berlin", "Dresden", "Leipzig"], "distance_km": 130},
            ],
        }
        recommendation = recommend_reroute(context)
        assert "action" in recommendation
        assert recommendation["action"] == "reroute"

    def test_driver_reassignment(self):
        """Test driver reassignment logic"""
        from decision_engine.driver_reassignment import recommend_driver_change

        context = {
            "current_driver_rating": 3.5,
            "available_drivers": [
                {"driver_id": "DRV001", "rating": 4.8},
                {"driver_id": "DRV002", "rating": 4.5},
            ],
            "delivery_priority": "high",
        }
        recommendation = recommend_driver_change(context)
        assert "action" in recommendation
        assert "driver_id" in recommendation

    def test_cost_benefit_calculation(self):
        """Test cost-benefit analysis"""
        from decision_engine.cost_benefit import calculate_impact

        action = {
            "action": "reroute",
            "additional_distance_km": 15,
            "estimated_time_savings_min": 20,
        }
        cost_benefit = calculate_impact(action)
        assert "cost" in cost_benefit
        assert "benefit" in cost_benefit

    def test_priority_queue_ordering(self):
        """Test priority queue orders deliveries correctly"""
        from decision_engine.priority_queue import PriorityQueue

        queue = PriorityQueue()
        deliveries = [
            {"delivery_id": "D1", "priority": "low", "delay_probability": 0.3},
            {"delivery_id": "D2", "priority": "high", "delay_probability": 0.8},
            {"delivery_id": "D3", "priority": "medium", "delay_probability": 0.5},
        ]
        for d in deliveries:
            queue.push(d)
        # High priority should come first
        first = queue.pop()
        assert first["priority"] == "high"
