# Milestone #237: Build Alert Generation

**Your Role:** AI/LLM Engineer

Create alert messages:

```python
# src/anomaly/alert_generator.py

from typing import Dict, List
from datetime import datetime

class AlertGenerator:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        return {
            "delay_rate_high": {
                "title": "High Delay Rate Alert",
                "template": "Delay rate is {current:.1%}, exceeding threshold of {threshold:.1%}",
                "severity": "high"
            },
            "avg_delay_high": {
                "title": "Average Delay Spike",
                "template": "Average delay is {current:.0f} minutes, threshold: {threshold:.0f} minutes",
                "severity": "medium"
            },
            "driver_shortage": {
                "title": "Driver Shortage Warning",
                "template": "Only {current} drivers available, minimum required: {threshold}",
                "severity": "critical"
            },
            "delivery_drop": {
                "title": "Delivery Volume Drop",
                "template": "Only {current} deliveries in last hour, expected: {threshold}+",
                "severity": "medium"
            },
            "anomaly_detected": {
                "title": "Anomaly Detected",
                "template": "Unusual pattern detected in {metric}. Score: {current:.2f}",
                "severity": "high"
            }
        }
    
    def generate_alert(self, trigger: Dict, context: Dict = None) -> Dict:
        metric = trigger["metric"]
        
        template_key = self._get_template_key(metric)
        template = self.templates.get(template_key, self.templates["anomaly_detected"])
        
        message = template["template"].format(
            current=trigger["current"],
            threshold=trigger["threshold"],
            metric=metric
        )
        
        return {
            "alert_id": f"alert_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": template["title"],
            "message": message,
            "severity": template["severity"],
            "metric": metric,
            "value": trigger["current"],
            "threshold": trigger["threshold"],
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
    
    def _get_template_key(self, metric: str) -> str:
        mapping = {
            "delay_rate": "delay_rate_high",
            "avg_delay": "avg_delay_high",
            "driver_count": "driver_shortage",
            "delivery_count": "delivery_drop"
        }
        return mapping.get(metric, "anomaly_detected")
```

Commit.