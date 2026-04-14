"""
Recommendations API endpoint.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/recommend", tags=["recommendations"])


class RecommendationRequest(BaseModel):
    """Request for recommendations."""

    order_id: str = Field(..., description="Order ID")
    delay_probability: float = Field(
        ..., ge=0, le=1, description="Predicted delay probability"
    )
    current_route: Optional[str] = Field(None, description="Current route ID")
    current_driver: Optional[str] = Field(None, description="Current driver ID")


class RecommendationAction(BaseModel):
    """Recommended action."""

    action: str
    priority: str
    description: str
    estimated_impact: str


class RecommendationResponse(BaseModel):
    """Response for recommendations."""

    order_id: str
    recommendations: List[RecommendationAction]


@router.post("", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get action recommendations for a delivery."""
    logger.info(f"Getting recommendations for order: {request.order_id}")

    recommendations = []

    if request.delay_probability > 0.5:
        recommendations.append(
            RecommendationAction(
                action="reroute",
                priority="high",
                description="Switch to alternate route via A10 (adds 3km but avoids flood zone)",
                estimated_impact="-12 minutes delay",
            )
        )

        recommendations.append(
            RecommendationAction(
                action="reassign_driver",
                priority="medium",
                description="Assign driver with higher on-time rating",
                estimated_impact="-5 minutes delay",
            )
        )

        recommendations.append(
            RecommendationAction(
                action="notifyCustomer",
                priority="low",
                description="Send proactive delay notification",
                estimated_impact="Customer satisfaction +10%",
            )
        )
    else:
        recommendations.append(
            RecommendationAction(
                action="notifyCustomer",
                priority="low",
                description="Confirm on-time delivery",
                estimated_impact="Customer satisfaction +5%",
            )
        )

    return RecommendationResponse(
        order_id=request.order_id, recommendations=recommendations
    )


@router.get("/actions")
async def get_available_actions():
    """Get available action types."""
    return {
        "actions": [
            {
                "id": "reroute",
                "name": "Reroute",
                "description": "Switch to an alternate route",
            },
            {
                "id": "reassign_driver",
                "name": "Reassign Driver",
                "description": "Assign a different driver",
            },
            {
                "id": "notify_customer",
                "name": "Notify Customer",
                "description": "Send customer notification",
            },
            {
                "id": "reschedule",
                "name": "Reschedule",
                "description": "Change delivery time window",
            },
        ]
    }
