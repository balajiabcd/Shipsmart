from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AlertThreshold:
    metric: str
    operator: str
    value: float
    duration_minutes: int = 0


class ThresholdManager:
    def __init__(self):
        self.thresholds: Dict[str, List[AlertThreshold]] = {}
        self._setup_default_thresholds()

    def _setup_default_thresholds(self):
        self.add_threshold("delay_rate", "gt", 0.5, duration_minutes=30)
        self.add_threshold("delay_rate", "gt", 0.8, duration_minutes=0)
        self.add_threshold("avg_delay", "gt", 60, duration_minutes=60)
        self.add_threshold("delivery_count", "lt", 10, duration_minutes=120)
        self.add_threshold("driver_count", "lt", 5, duration_minutes=60)
        self.add_threshold("anomaly_score", "gt", 0.8, duration_minutes=0)

    def add_threshold(
        self, metric: str, operator: str, value: float, duration_minutes: int = 0
    ):
        if metric not in self.thresholds:
            self.thresholds[metric] = []

        self.thresholds[metric].append(
            AlertThreshold(
                metric=metric,
                operator=operator,
                value=value,
                duration_minutes=duration_minutes,
            )
        )

    def remove_threshold(self, metric: str, operator: str, value: float):
        if metric in self.thresholds:
            self.thresholds[metric] = [
                t
                for t in self.thresholds[metric]
                if not (t.operator == operator and t.value == value)
            ]

    def check_thresholds(
        self, current_values: Dict[str, float], history: Dict[str, List] = None
    ) -> List[Dict]:
        triggered = []

        for metric, thresholds in self.thresholds.items():
            current = current_values.get(metric)
            if current is None:
                continue

            for thresh in thresholds:
                if self._evaluate_condition(current, thresh.operator, thresh.value):
                    if thresh.duration_minutes > 0 and history:
                        if self._check_sustained(metric, current, thresh, history):
                            triggered.append(
                                {
                                    "metric": metric,
                                    "threshold": thresh.value,
                                    "current": current,
                                    "operator": thresh.operator,
                                    "duration": thresh.duration_minutes,
                                    "type": "sustained",
                                }
                            )
                    elif thresh.duration_minutes == 0:
                        triggered.append(
                            {
                                "metric": metric,
                                "threshold": thresh.value,
                                "current": current,
                                "operator": thresh.operator,
                                "type": "immediate",
                            }
                        )

        return triggered

    def _evaluate_condition(
        self, current: float, operator: str, threshold: float
    ) -> bool:
        if operator == "gt":
            return current > threshold
        if operator == "lt":
            return current < threshold
        if operator == "eq":
            return current == threshold
        if operator == "gte":
            return current >= threshold
        if operator == "lte":
            return current <= threshold
        return False

    def _check_sustained(
        self, metric: str, current: float, threshold: AlertThreshold, history: Dict
    ) -> bool:
        values = history.get(metric, [])
        window = values[-min(threshold.duration_minutes, len(values)) :]
        return len([v for v in window if v > threshold.value]) > 0

    def get_thresholds(self, metric: Optional[str] = None) -> Dict:
        if metric:
            return {metric: self.thresholds.get(metric, [])}
        return self.thresholds

    def clear_thresholds(self, metric: Optional[str] = None):
        if metric:
            self.thresholds.pop(metric, None)
        else:
            self.thresholds.clear()


if __name__ == "__main__":
    manager = ThresholdManager()
    print(f"Default thresholds: {list(manager.thresholds.keys())}")
