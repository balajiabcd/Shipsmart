# Milestone #257: Create Prediction Request Models

**Your Role:** Full-Stack Dev

Pydantic models:

```python
# api/models/prediction.py

from pydantic import BaseModel, Field
from typing import Optional, List

class DeliveryFeatures(BaseModel):
    distance_km: float = Field(..., ge=0)
    weather_condition: str
    weather_severity: int = Field(..., ge=0, le=10)
    traffic_index: int = Field(..., ge=0, le=10)
    time_of_day: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    driver_performance: float = Field(..., ge=0, le=1)
    vehicle_type: str
    warehouse_load: float = Field(..., ge=0, le=1)

class PredictionRequest(BaseModel):
    delivery_id: str
    features: DeliveryFeatures
    include_factors: bool = True
    include_explanation: bool = False

class BatchPredictionRequest(BaseModel):
    deliveries: List[PredictionRequest]
```

Commit.