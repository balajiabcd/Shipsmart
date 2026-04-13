# Milestone #258: Create Prediction Response Models

**Your Role:** Full-Stack Dev

Output schemas:

```python
# api/models/response.py

from pydantic import BaseModel
from typing import Optional, List

class PredictionResponse(BaseModel):
    delivery_id: str
    prediction: str  # "delayed" or "on_time"
    confidence: float
    delay_probability: float

class PredictionWithFactorsResponse(PredictionResponse):
    top_factors: List[dict]
    feature_importance: dict

class ExplanationResponse(PredictionResponse):
    explanation: str
    root_cause: List[str]
    confidence_level: str
```

# Milestone #259: Implement /predict Endpoint

```python
# api/endpoints/predict.py

from fastapi import APIRouter, HTTPException
import joblib

router = APIRouter(prefix="/predict", tags=["Predictions"])

@router.post("/")
async def predict_delivery(request: PredictionRequest):
    try:
        model = joblib.load('models/best_classifier.pkl')
        
        features = [list(request.features.dict().values())]
        proba = model.predict_proba(features)[0]
        
        return PredictionResponse(
            delivery_id=request.delivery_id,
            prediction="delayed" if proba[1] > 0.5 else "on_time",
            confidence=max(proba),
            delay_probability=proba[1]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Commit both.