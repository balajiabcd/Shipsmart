"""
Alerts API endpoint.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/alerts", tags=["alerts"])


class Alert(BaseModel):
    """Alert information."""

    alert_id: str
    type: str
    severity: str
    message: str
    timestamp: str
    region: Optional[str] = None
    possible_causes: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)


class AlertsResponse(BaseModel):
    """Response with alerts."""

    alerts: List[Alert]
    count: int
    high_severity_count: int


@router.get("", response_model=AlertsResponse)
async def get_alerts(
    severity: Optional[str] = None, region: Optional[str] = None, limit: int = 50
):
    """Get active alerts."""
    logger.info(f"Getting alerts (severity={severity}, region={region})")

    alerts = [
        Alert(
            alert_id="ALERT-001",
            type="anomaly",
            severity="high",
            message="Munich region has experienced 35% increase in delays",
            timestamp=datetime.now().isoformat(),
            region="munich",
            possible_causes=["Road closure", "Festival", "Staff shortage"],
            recommended_actions=["Review routes", "Alert manager"],
        ),
        Alert(
            alert_id="ALERT-002",
            type="weather",
            severity="medium",
            message="Heavy rain expected in Berlin region",
            timestamp=datetime.now().isoformat(),
            region="berlin",
            possible_causes=["Storm"],
            recommended_actions=["Notify drivers"],
        ),
    ]

    if severity:
        alerts = [a for a in alerts if a.severity == severity]
    if region:
        alerts = [a for a in alerts if a.region == region]

    high_count = sum(1 for a in alerts if a.severity == "high")

    return AlertsResponse(
        alerts=alerts[:limit], count=len(alerts), high_severity_count=high_count
    )


@router.get("/{alert_id}")
async def get_alert(alert_id: str):
    """Get specific alert."""
    logger.info(f"Getting alert: {alert_id}")

    return Alert(
        alert_id=alert_id,
        type="anomaly",
        severity="high",
        message="Sample alert message",
        timestamp=datetime.now().isoformat(),
        possible_causes=["Cause 1"],
        recommended_actions=["Action 1"],
    )


@router.post("/acknowledge/{alert_id}")
async def acknowledge_alert(alert_id: str):
    """Acknowledge an alert."""
    logger.info(f"Acknowledging alert: {alert_id}")

    return {
        "alert_id": alert_id,
        "status": "acknowledged",
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/statistics/summary")
async def get_alert_statistics():
    """Get alert statistics."""
    return {
        "total_alerts": 15,
        "active_alerts": 2,
        "acknowledged_alerts": 13,
        "by_severity": {"high": 5, "medium": 7, "low": 3},
        "by_type": {"anomaly": 8, "weather": 4, "operational": 3},
    }
