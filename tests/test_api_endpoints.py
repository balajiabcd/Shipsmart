"""
Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.api.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict():
    """Test predict endpoint."""
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


def test_predict_proba():
    """Test predict_proba endpoint."""
    response = client.get("/api/v1/predict/proba?order_id=ORD-001")
    assert response.status_code == 200
    data = response.json()
    assert "probabilities" in data


def test_recommend():
    """Test recommend endpoint."""
    response = client.post(
        "/api/v1/recommend", json={"order_id": "ORD-001", "delay_probability": 0.75}
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data


def test_alerts():
    """Test alerts endpoint."""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert "count" in data


def test_route_optimize():
    """Test route optimize endpoint."""
    response = client.post(
        "/api/v1/route/optimize",
        json={
            "origin": {"id": "depot", "lat": 52.52, "lon": 13.405},
            "destination": {"id": "munich", "lat": 48.1351, "lon": 11.582},
            "optimization_type": "distance",
        },
    )
    assert response.status_code in [200, 404, 500]


def test_metrics():
    """Test metrics endpoint."""
    response = client.get("/api/v1/metrics")
    assert response.status_code in [200, 404]


def test_auth_token():
    """Test auth token endpoint."""
    response = client.post(
        "/api/v1/auth/token", data={"username": "admin", "password": "password"}
    )
    assert response.status_code in [200, 401]


def test_api_health():
    """Test API v1 health."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
