from typing import Dict, List, Optional
from datetime import datetime


class AlertGenerator:
    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        return {
            "delay_rate_high": {
                "title": "High Delay Rate Alert",
                "template": "Delay rate is {current:.1%}, exceeding threshold of {threshold:.1%}",
                "severity": "high",
            },
            "avg_delay_high": {
                "title": "Average Delay Spike",
                "template": "Average delay is {current:.0f} minutes, threshold: {threshold:.0f} minutes",
                "severity": "medium",
            },
            "driver_shortage": {
                "title": "Driver Shortage Warning",
                "template": "Only {current} drivers available, minimum required: {threshold}",
                "severity": "critical",
            },
            "delivery_drop": {
                "title": "Delivery Volume Drop",
                "template": "Only {current} deliveries in last hour, expected: {threshold}+",
                "severity": "medium",
            },
            "anomaly_detected": {
                "title": "Anomaly Detected",
                "template": "Unusual pattern detected in {metric}. Score: {current:.2f}",
                "severity": "high",
            },
        }

    def generate_alert(self, trigger: Dict, context: Dict = None) -> Dict:
        metric = trigger.get("metric", "unknown")

        template_key = self._get_template_key(metric)
        template = self.templates.get(template_key, self.templates["anomaly_detected"])

        try:
            message = template["template"].format(
                current=trigger.get("current", 0),
                threshold=trigger.get("threshold", 0),
                metric=metric,
            )
        except:
            message = f"Anomaly detected: {metric} = {trigger.get('current', 0)}"

        return {
            "alert_id": f"alert_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "title": template["title"],
            "message": message,
            "severity": template["severity"],
            "metric": metric,
            "value": trigger.get("current", 0),
            "threshold": trigger.get("threshold", 0),
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "type": trigger.get("type", "immediate"),
        }

    def generate_batch(self, triggers: List[Dict], context: Dict = None) -> List[Dict]:
        return [self.generate_alert(t, context) for t in triggers]

    def _get_template_key(self, metric: str) -> str:
        mapping = {
            "delay_rate": "delay_rate_high",
            "avg_delay": "avg_delay_high",
            "driver_count": "driver_shortage",
            "delivery_count": "delivery_drop",
            "anomaly_score": "anomaly_detected",
        }
        return mapping.get(metric, "anomaly_detected")

    def add_template(self, key: str, title: str, template: str, severity: str):
        self.templates[key] = {
            "title": title,
            "template": template,
            "severity": severity,
        }

    def get_severity_levels(self) -> List[str]:
        return ["critical", "high", "medium", "low"]


if __name__ == "__main__":
    generator = AlertGenerator()
    print(f"Alert generator ready with {len(generator.templates)} templates")
