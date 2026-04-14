# Milestone #164: Create Recommendation API Endpoint

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
Expose recommendation endpoint:

```python
# api/endpoints/recommendations.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

class DeliveryContext(BaseModel):
    delivery_id: str
    origin: str
    destination: str
    scheduled_time: str
    driver_id: Optional[str] = None
    vehicle_type: Optional[str] = None
    is_fragile: bool = False
    customer_tier: str = "standard"

@router.post("/")
async def get_recommendations(context: DeliveryContext):
    """Get actionable recommendations for a delivery"""
    
    try:
        model = joblib.load('models/best_classifier.pkl')
        
        features = extract_features(context)
        prediction = model.predict_proba([features])
        
        decision_context = {
            **context.dict(),
            "delay_probability": prediction[1],
            "top_factors": get_top_factors(features)
        }
        
        triggered_rules = evaluate_rules(decision_context)
        recommendations = generate_recommendations(
            prediction, triggered_rules, decision_context
        )
        
        ranked = rank_recommendations(recommendations, decision_context)
        
        return {
            "delivery_id": context.delivery_id,
            "delay_probability": float(prediction[1]),
            "risk_level": "high" if prediction[1] > 0.7 else "medium" if prediction[1] > 0.4 else "low",
            "recommendations": ranked[:5],
            "should_intervene": prediction[1] > 0.5
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/priority-queue")
async def get_priority_queue():
    """Get prioritized list of deliveries needing attention"""
    # Return from priority queue
    return {"queue": get_queued_deliveries()}
```

**Completed:**
- Created `src/api/endpoints/recommendations.py` with endpoints:
  - `POST /recommend/` - Single delivery recommendations
  - `POST /recommend/batch` - Batch recommendations
  - `GET /recommend/priority-queue` - Get priority queue
  - `POST /recommend/priority-queue/enqueue` - Add to queue
  - `GET /recommend/health` - Health check

**Milestones 155-164 COMPLETED**

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #165: Test Decision Engine
- Create unit tests for decision logic
- Validate recommendations