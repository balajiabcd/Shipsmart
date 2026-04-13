# Milestone #215: Create /explain API Endpoint

**Your Role:** AI/LLM Engineer

Expose explanation service:

```python
# api/endpoints/explain.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import joblib

router = APIRouter(prefix="/explain", tags=["Explainability"])

class ExplainRequest(BaseModel):
    delivery_id: str
    include_factors: bool = True
    format: str = "text"  # text, json, markdown

class ExplanationResponse(BaseModel):
    delivery_id: str
    prediction: float
    explanation: str
    root_causes: List[str]
    confidence: str

@router.post("/", response_model=ExplanationResponse)
async def explain_prediction(request: ExplainRequest):
    try:
        model = joblib.load('models/best_classifier.pkl')
        shap_explainer = joblib.load('models/shap_explainer.pkl')
        
        features = extract_features_for_delivery(request.delivery_id)
        
        prob = model.predict_proba([features])[0][1]
        
        if request.include_factors:
            shap_values = shap_explainer.shap_values([features])
            factors = format_shap_factors(shap_values, features.columns)
            causes = extract_root_causes(shap_values)
        else:
            factors = []
            causes = []
        
        explanation = generate_nl_explanation(factors, features, request.format)
        
        return ExplanationResponse(
            delivery_id=request.delivery_id,
            prediction=float(prob),
            explanation=explanation,
            root_causes=causes,
            confidence="high" if prob > 0.8 or prob < 0.2 else "medium"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/root-causes/{delivery_id}")
async def get_root_causes(delivery_id: str):
    """Get just the root causes without full explanation"""
    # Simplified endpoint
    return {"delivery_id": delivery_id, "root_causes": []}
```

Add to `api/main.py`. Commit.