from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import numpy as np


router = APIRouter(prefix="/explain", tags=["Explainability"])


class ExplainRequest(BaseModel):
    delivery_id: str
    include_factors: bool = True
    format: str = "text"


class ExplanationResponse(BaseModel):
    delivery_id: str
    prediction: float
    explanation: str
    root_causes: List[str]
    confidence: str


@router.post("/", response_model=ExplanationResponse)
async def explain_prediction(request: ExplainRequest):
    try:
        from src.root_cause.shap_llm_integration import SHAPLLMIntegrator
        from src.root_cause.generator import NLExplanationGenerator

        integrator = SHAPLLMIntegrator()

        context = {
            "delivery_id": request.delivery_id,
            "weather": "unknown",
            "traffic": "unknown",
            "distance": 0,
        }

        result = integrator.explain_prediction(
            pd.DataFrame([{"feature": "value"}]), context
        )

        result["delivery_id"] = request.delivery_id
        result["explanation"] = result.get("explanation", "Explanation generated")
        result["root_causes"] = result.get("root_causes", [])

        prob = result.get("prediction", 0.5)
        result["confidence"] = "high" if prob > 0.8 or prob < 0.2 else "medium"

        return result

    except Exception as e:
        return ExplanationResponse(
            delivery_id=request.delivery_id,
            prediction=0.5,
            explanation=f"Error generating explanation: {str(e)}",
            root_causes=[],
            confidence="low",
        )


@router.get("/root-causes/{delivery_id}")
async def get_root_causes(delivery_id: str):
    return {"delivery_id": delivery_id, "root_causes": []}


@router.get("/factors/{delivery_id}")
async def get_shap_factors(delivery_id: str):
    return {
        "delivery_id": delivery_id,
        "shap_values": [],
        "message": "SHAP factors available when model is loaded",
    }


import pandas as pd
