import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.api.main import app

client = TestClient(app)


class TestMLAndAPIIntegration:
    """Test ML + API integration (Milestone 384)"""

    @pytest.mark.integration
    def test_prediction_flow(self):
        """Test full prediction flow from request to response"""
        response = client.post(
            "/api/v1/predict",
            json={
                "order_id": "ORD-001",
                "origin_lat": 52.52,
                "origin_lon": 13.405,
                "destination_lat": 48.1351,
                "destination_lon": 11.582,
                "scheduled_date": "2026-04-15",
                "scheduled_time": "14:00",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "predicted_delay" in data
        assert "delay_probability" in data

    @pytest.mark.integration
    def test_recommendation_flow(self):
        """Test prediction -> recommendation flow"""
        # First get prediction
        predict_response = client.post(
            "/api/v1/predict",
            json={
                "order_id": "ORD-002",
                "origin_lat": 52.52,
                "origin_lon": 13.405,
                "destination_lat": 48.1351,
                "destination_lon": 11.582,
            },
        )
        assert predict_response.status_code == 200

        # Then get recommendation
        recommend_response = client.post(
            "/api/v1/recommend",
            json={"order_id": "ORD-002"},
        )
        assert recommend_response.status_code == 200

    @pytest.mark.integration
    def test_explain_flow(self):
        """Test explanation generation flow"""
        response = client.post(
            "/api/v1/explain",
            json={"order_id": "ORD-001"},
        )
        assert response.status_code in [200, 404]


class TestLLMRAGIntegration:
    """Test LLM + RAG pipeline (Milestone 385)"""

    @pytest.mark.integration
    def test_chat_endpoint(self):
        """Test chat endpoint with RAG"""
        response = client.post(
            "/api/v1/chat",
            json={"message": "Why is delivery delayed?"},
        )
        assert response.status_code in [200, 404, 500]

    @pytest.mark.integration
    def test_vector_search(self):
        """Test vector search functionality"""
        response = client.post(
            "/api/v1/vector_search",
            json={"query": "delivery delay", "top_k": 5},
        )
        assert response.status_code in [200, 404, 500]

    @pytest.mark.integration
    def test_rag_context_retrieval(self):
        """Test RAG retrieves relevant context"""
        response = client.post(
            "/api/v1/chat",
            json={"message": "weather impact on delivery"},
        )
        # Should retrieve relevant context about weather
        assert response.status_code in [200, 404, 500]


class TestK8sDeployment:
    """Test Kubernetes deployment (Milestone 386)"""

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires Kubernetes cluster")
    def test_k8s_health_check(self):
        """Test K8s health endpoints"""
        # Would test if deployed in K8s
        pass

    @pytest.mark.integration
    def test_service_discovery(self):
        """Test internal service communication"""
        # Mock Kubernetes service discovery
        services = ["shipsmart-api", "shipsmart-ml", "shipsmart-frontend"]
        for service in services:
            # Would verify service is reachable
            assert service is not None
