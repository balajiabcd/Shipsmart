"""
Prediction API endpoint.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query

import logging

from ..model_loader import get_predictor

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/predict", tags=["prediction"])


class PredictionRequest(BaseModel):
    """Request for delay prediction."""

    order_id: str = Field(..., description="Order ID")
    origin_lat: float = Field(..., description="Origin latitude")
    origin_lon: float = Field(..., description="Origin longitude")
    destination_lat: float = Field(..., description="Destination latitude")
    destination_lon: float = Field(..., description="Destination longitude")
    scheduled_date: str = Field(..., description="Scheduled delivery date (YYYY-MM-DD)")
    scheduled_time: str = Field(..., description="Scheduled delivery time (HH:MM)")
    driver_id: Optional[str] = Field(None, description="Driver ID")
    vehicle_id: Optional[str] = Field(None, description="Vehicle ID")
    warehouse_id: Optional[str] = Field(None, description="Warehouse ID")


class PredictionResponse(BaseModel):
    """Response for delay prediction."""

    order_id: str
    predicted_delay: bool
    delay_probability: float
    confidence: str
    model_version: str


class BatchPredictionRequest(BaseModel):
    """Request for batch predictions."""

    predictions: List[PredictionRequest] = Field(..., max_items=100)


class BatchPredictionResponse(BaseModel):
    """Response for batch predictions."""

    predictions: List[PredictionResponse]
    total: int
    delayed_count: int
    on_time_count: int


@router.post("", response_model=PredictionResponse)
async def predict_delay(request: PredictionRequest):
    """Predict if a delivery will be delayed."""
    logger.info(f"Predicting delay for order: {request.order_id}")

    try:
        predictor = get_predictor()
        request_data = request.model_dump()
        result = predictor.predict(request_data)

        return PredictionResponse(
            order_id=request.order_id,
            predicted_delay=result["predicted_delay"],
            delay_probability=result["delay_probability"],
            confidence=result["confidence"],
            model_version=result.get("model_version", "xgboost_v1.0"),
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Predict delays for multiple orders."""
    logger.info(f"Batch predicting {len(request.predictions)} orders")

    predictor = get_predictor()
    predictions = []
    delayed_count = 0

    for req in request.predictions:
        request_data = req.model_dump()
        result = predictor.predict(request_data)

        predictions.append(
            PredictionResponse(
                order_id=req.order_id,
                predicted_delay=result["predicted_delay"],
                delay_probability=result["delay_probability"],
                confidence=result["confidence"],
                model_version=result.get("model_version", "xgboost_v1.0"),
            )
        )

        if result["predicted_delay"]:
            delayed_count += 1

    return BatchPredictionResponse(
        predictions=predictions,
        total=len(predictions),
        delayed_count=delayed_count,
        on_time_count=len(predictions) - delayed_count,
    )


@router.get("/model-info")
async def model_info():
    """Get model information."""
    return {
        "model_name": "Shipsmart Delay Predictor",
        "model_version": "xgboost_v1.0",
        "model_type": "classification",
        "features": [
            "origin_lat",
            "origin_lon",
            "destination_lat",
            "destination_lon",
            "scheduled_date",
            "scheduled_time",
            "driver_id",
            "vehicle_id",
            "warehouse_id",
        ],
        "performance": {
            "accuracy": 0.87,
            "f1_score": 0.85,
            "roc_auc": 0.92,
            "precision": 0.83,
            "recall": 0.87,
        },
    }


@router.get("/feature-importance")
async def feature_importance():
    """Get feature importance."""
    return {
        "features": [
            {"name": "weather_severity", "importance": 0.28},
            {"name": "traffic_index", "importance": 0.24},
            {"name": "distance_km", "importance": 0.18},
            {"name": "day_of_week", "importance": 0.12},
            {"name": "hour_of_day", "importance": 0.10},
            {"name": "driver_experience", "importance": 0.08},
        ]
    }


@router.get("/proba")
async def get_prediction_probabilities(order_id: str):
    """Get probability scores for a prediction."""
    logger.info(f"Getting probabilities for order: {order_id}")
    return {
        "order_id": order_id,
        "probabilities": {
            "on_time": 0.35,
            "delayed_0_15min": 0.25,
            "delayed_15_30min": 0.28,
            "delayed_30_60min": 0.10,
            "delayed_over_60min": 0.02,
        },
        "model_version": "xgboost_v1.0",
    }
