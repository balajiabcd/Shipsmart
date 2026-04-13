# Milestone #236: Create Alert Threshold Logic

**Your Role:** AI/LLM Engineer

Define alert triggers:

```python
# src/anomaly/thresholds.py

from dataclasses import dataclass
from typing import Dict

@dataclass
class AlertThreshold:
    metric: str
    operator: str  # gt, lt, eq
    value: float
    duration_minutes: int = 0  # For sustained anomalies

class ThresholdManager:
    def __init__(self):
        self.thresholds = {}
        self._setup_default_thresholds()
    
    def _setup_default_thresholds(self):
        self.add_threshold("delay_rate", "gt", 0.5, duration_minutes=30)
        self.add_threshold("delay_rate", "gt", 0.8, duration_minutes=0)
        self.add_threshold("avg_delay", "gt", 60, duration_minutes=60)
        self.add_threshold("delivery_count", "lt", 10, duration_minutes=120)
        self.add_threshold("driver_count", "lt", 5, duration_minutes=60)
        self.add_threshold("anomaly_score", "gt", 0.8, duration_minutes=0)
    
    def add_threshold(self, metric: str, operator: str, value: float, duration_minutes: int = 0):
        if metric not in self.thresholds:
            self.thresholds[metric] = []
        
        self.thresholds[metric].append(AlertThreshold(
            metric=metric, operator=operator, value=value, duration_minutes=duration_minutes
        ))
    
    def check_thresholds(self, current_values: Dict[str, float], history: Dict[str, list] = None) -> list:
        triggered = []
        
        for metric, thresholds in self.thresholds.items():
            current = current_values.get(metric)
            if current is None:
                continue
            
            for thresh in thresholds:
                if self._evaluate_condition(current, thresh.operator, thresh.value):
                    if thresh.duration_minutes > 0 and history:
                        if self._check_sustained(metric, current, thresh, history):
                            triggered.append({
                                "metric": metric,
                                "threshold": thresh.value,
                                "current": current,
                                "operator": thresh.operator
                            })
                    elif thresh.duration_minutes == 0:
                        triggered.append({
                            "metric": metric,
                            "threshold": thresh.value,
                            "current": current,
                            "operator": thresh.operator
                        })
        
        return triggered
    
    def _evaluate_condition(self, current: float, operator: str, threshold: float) -> bool:
        if operator == "gt": return current > threshold
        if operator == "lt": return current < threshold
        if operator == "eq": return current == threshold
        return False
    
    def _check_sustained(self, metric: str, current: float, threshold: AlertThreshold, history: Dict) -> bool:
        values = history.get(metric, [])
        return len([v for v in values[-threshold.duration_minutes:] if v > threshold.value]) > 0
```

Commit.