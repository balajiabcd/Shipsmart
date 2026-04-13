# Milestone #240: Create /alerts API Endpoint

**Your Role:** AI/LLM Engineer

Expose alert service:

```python
# api/endpoints/alerts.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["Alerts"])

class AlertResponse(BaseModel):
    alert_id: str
    title: str
    message: str
    severity: str
    metric: str
    value: float
    threshold: float
    timestamp: str

class AlertQuery(BaseModel):
    severity: Optional[str] = None
    metric: Optional[str] = None
    from_time: Optional[str] = None
    limit: int = 50

alerts_store = []  # Use database in production

@router.post("/", response_model=AlertResponse)
async def create_alert(alert: dict):
    alerts_store.append(alert)
    return alert

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(query: AlertQuery):
    filtered = alerts_store
    
    if query.severity:
        filtered = [a for a in filtered if a.get("severity") == query.severity]
    if query.metric:
        filtered = [a for a in filtered if a.get("metric") == query.metric]
    if query.from_time:
        filtered = [a for a in filtered if a.get("timestamp", "") >= query.from_time]
    
    return filtered[:query.limit]

@router.get("/{alert_id}")
async def get_alert(alert_id: str):
    for alert in alerts_store:
        if alert.get("alert_id") == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")

@router.get("/summary")
async def get_alert_summary():
    return {
        "total": len(alerts_store),
        "critical": len([a for a in alerts_store if a.get("severity") == "critical"]),
        "high": len([a for a in alerts_store if a.get("severity") == "high"]),
        "medium": len([a for a in alerts_store if a.get("severity") == "medium"]),
        "low": len([a for a in alerts_store if a.get("severity") == "low"])
    }
```

Add to `api/main.py`. Commit.