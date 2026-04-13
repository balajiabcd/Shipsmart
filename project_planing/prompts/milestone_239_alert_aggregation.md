# Milestone #239: Implement Alert Aggregation

**Your Role:** AI/LLM Engineer

Group related alerts:

```python
# src/anomaly/aggregation.py

from typing import List, Dict
from datetime import datetime, timedelta
import hashlib

class AlertAggregator:
    def __init__(self, window_minutes: int = 60):
        self.window = timedelta(minutes=window_minutes)
        self.active_groups = {}
    
    def aggregate(self, alerts: List[Dict]) -> List[Dict]:
        groups = {}
        
        for alert in alerts:
            group_key = self._get_group_key(alert)
            
            if group_key not in groups:
                groups[group_key] = {
                    "group_id": group_key,
                    "alerts": [],
                    "severity": alert.get("severity", "medium"),
                    "first_seen": alert["timestamp"],
                    "last_seen": alert["timestamp"],
                    "count": 0
                }
            
            groups[group_key]["alerts"].append(alert)
            groups[group_key]["count"] += 1
            
            if alert["timestamp"] > groups[group_key]["last_seen"]:
                groups[group_key]["last_seen"] = alert["timestamp"]
        
        return list(groups.values())
    
    def _get_group_key(self, alert: Dict) -> str:
        key_parts = [
            alert.get("metric", ""),
            alert.get("severity", ""),
            alert.get("location", "global")
        ]
        
        key_str = "_".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()[:8]
    
    def create_summary(self, groups: List[Dict]) -> Dict:
        return {
            "total_alerts": sum(g["count"] for g in groups),
            "groups": len(groups),
            "critical_count": len([g for g in groups if g["severity"] == "critical"]),
            "high_count": len([g for g in groups if g["severity"] == "high"]),
            "by_metric": self._group_by_metric(groups)
        }
    
    def _group_by_metric(self, groups: List[Dict]) -> Dict:
        by_metric = {}
        for g in groups:
            metric = g["alerts"][0].get("metric", "unknown")
            if metric not in by_metric:
                by_metric[metric] = 0
            by_metric[metric] += g["count"]
        return by_metric
```

Commit.