from enum import Enum
from typing import List, Dict


class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SeverityClassifier:
    def __init__(self):
        self.critical_metrics = {"driver_count", "anomaly_score"}
        self.high_metrics = {"delay_rate", "avg_delay"}
        self.medium_metrics = {"delivery_count", "weather_severity"}

    def classify(self, alert: Dict) -> str:
        metric = alert.get("metric", "")

        if metric in self.critical_metrics:
            return self._classify_critical(alert)
        elif metric in self.high_metrics:
            return self._classify_high(alert)
        elif metric in self.medium_metrics:
            return self._classify_medium(alert)

        return "low"

    def _classify_critical(self, alert: Dict) -> str:
        if alert.get("value", 0) < 3:
            return "critical"
        return "high"

    def _classify_high(self, alert: Dict) -> str:
        if alert.get("value", 0) > 0.8:
            return "critical"
        elif alert.get("value", 0) > 0.6:
            return "high"
        return "medium"

    def _classify_medium(self, alert: Dict) -> str:
        return "medium"

    def prioritize_alerts(self, alerts: List[Dict]) -> List[Dict]:
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

        for alert in alerts:
            alert["severity"] = self.classify(alert)

        return sorted(
            alerts, key=lambda a: priority_order.get(a.get("severity", "low"), 3)
        )

    def get_severity_value(self, severity: str) -> int:
        values = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        return values.get(severity, 0)


if __name__ == "__main__":
    classifier = SeverityClassifier()
    print("Severity classifier ready")
