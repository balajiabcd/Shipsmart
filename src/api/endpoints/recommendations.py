from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging

from ..decision_engine.hybrid_engine import HybridDecisionEngine
from ..decision_engine.priority_queue import DeliveryPriorityQueue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

decision_engine = None
priority_queue = DeliveryPriorityQueue()


def get_decision_engine():
    global decision_engine
    if decision_engine is None:
        try:
            decision_engine = HybridDecisionEngine()
        except Exception as e:
            logger.error(f"Error initializing decision engine: {e}")
    return decision_engine


class DeliveryContext(BaseModel):
    delivery_id: str
    origin: str
    destination: str
    scheduled_time: str
    driver_id: Optional[str] = None
    vehicle_type: Optional[str] = None
    is_fragile: bool = False
    customer_tier: str = "standard"
    driver_performance: Optional[float] = None
    traffic_index: Optional[float] = None
    weather_severity: Optional[float] = None
    is_holiday: bool = False
    is_weekend: bool = False
    distance_km: Optional[float] = None


@router.post("/")
async def get_recommendations(context: DeliveryContext):
    """Get actionable recommendations for a delivery"""

    try:
        engine = get_decision_engine()

        features = context.dict()

        if engine:
            result = engine.predict(features)
        else:
            result = {
                "prediction": {"delay_probability": 0.3, "on_time_probability": 0.7},
                "risk_level": "low",
                "recommendations": [],
                "should_intervene": False,
            }

        return {
            "delivery_id": context.delivery_id,
            "delay_probability": result["prediction"].get("delay_probability", 0.3),
            "risk_level": result.get("risk_level", "low"),
            "recommendations": result.get("recommendations", [])[:5],
            "triggered_rules": result.get("triggered_rules", []),
            "should_intervene": result.get("should_intervene", False),
            "execution_plan": result.get("execution_plan", {}),
        }

    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def get_batch_recommendations(contexts: List[DeliveryContext]):
    """Get recommendations for multiple deliveries"""

    results = []

    engine = get_decision_engine()

    for context in contexts:
        try:
            if engine:
                result = engine.predict(context.dict())
            else:
                result = {
                    "prediction": {"delay_probability": 0.3},
                    "risk_level": "low",
                    "recommendations": [],
                    "should_intervene": False,
                }

            results.append(
                {
                    "delivery_id": context.delivery_id,
                    "delay_probability": result["prediction"].get(
                        "delay_probability", 0.3
                    ),
                    "risk_level": result.get("risk_level", "low"),
                    "should_intervene": result.get("should_intervene", False),
                    "recommendations": result.get("recommendations", [])[:3],
                }
            )
        except Exception as e:
            logger.error(f"Error for delivery {context.delivery_id}: {e}")
            results.append({"delivery_id": context.delivery_id, "error": str(e)})

    return {"results": results}


@router.get("/priority-queue")
async def get_priority_queue(limit: int = 10):
    """Get prioritized list of deliveries needing attention"""

    queue_items = priority_queue.get_next_batch(limit)

    return {
        "queue_size": priority_queue.get_size(),
        "high_risk_count": len(priority_queue.get_high_risk_deliveries()),
        "deliveries": [
            {
                "delivery_id": item.delivery_id,
                "priority": item.priority,
                "risk_level": item.risk_level,
                "delay_probability": item.context.get("delay_probability", 0),
            }
            for item in queue_items
        ],
    }


@router.post("/priority-queue/enqueue")
async def enqueue_delivery(context: DeliveryContext):
    """Add delivery to priority queue"""

    priority_queue.enqueue(context.delivery_id, context.dict())

    return {
        "delivery_id": context.delivery_id,
        "status": "enqueued",
        "queue_size": priority_queue.get_size(),
    }


@router.get("/health")
async def health_check():
    """Check decision engine health"""

    engine = get_decision_engine()

    return {
        "status": "healthy" if engine else "degraded",
        "model_loaded": engine is not None,
        "queue_size": priority_queue.get_size(),
    }
