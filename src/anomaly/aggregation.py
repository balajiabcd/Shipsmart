from typing import List, Dict
from datetime import datetime, timedelta
import hashlib


class AlertAggregator:
    def __init__(self, window_minutes: int = 60):
        self.window = timedelta(minutes=window_minutes)
        self.active_groups: Dict = {}

    def aggregate(self, alerts: List[Dict]) -> List[Dict]:
        groups: Dict = {}

        for alert in alerts:
            group_key = self._get_group_key(alert)
            severity = alert.get("severity", "medium")
            timestamp = alert.get("timestamp", datetime.now().isoformat())

            if group_key not in groups:
                groups[group_key] = {
                    "group_id": group_key,
                    "alerts": [],
                    "severity": severity,
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "count": 0,
                    "metric": alert.get("metric", "unknown"),
                }

            groups[group_key]["alerts"].append(alert)
            groups[group_key]["count"] += 1

            if timestamp > groups[group_key]["last_seen"]:
                groups[group_key]["last_seen"] = timestamp

            if severity == "critical":
                groups[group_key]["severity"] = "critical"
            elif severity == "high" and groups[group_key]["severity"] != "critical":
                groups[group_key]["severity"] = "high"

        return list(groups.values())

    def _get_group_key(self, alert: Dict) -> str:
        key_parts = [
            alert.get("metric", ""),
            alert.get("severity", ""),
            alert.get("location", "global"),
        ]

        key_str = "_".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()[:8]

    def create_summary(self, groups: List[Dict]) -> Dict:
        return {
            "total_alerts": sum(g["count"] for g in groups),
            "groups": len(groups),
            "critical_count": len([g for g in groups if g["severity"] == "critical"]),
            "high_count": len([g for g in groups if g["severity"] == "high"]),
            "medium_count": len([g for g in groups if g["severity"] == "medium"]),
            "low_count": len([g for g in groups if g["severity"] == "low"]),
            "by_metric": self._group_by_metric(groups),
        }

    def _group_by_metric(self, groups: List[Dict]) -> Dict:
        by_metric = {}
        for g in groups:
            metric = g.get("metric", "unknown")
            if metric not in by_metric:
                by_metric[metric] = 0
            by_metric[metric] += g["count"]
        return by_metric

    def get_active_groups(self) -> List[Dict]:
        return list(self.active_groups.values())

    def clear_old_groups(self, max_age_minutes: int = 60):
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        self.active_groups = {
            k: v
            for k, v in self.active_groups.items()
            if datetime.fromisoformat(v["last_seen"]) > cutoff
        }


if __name__ == "__main__":
    aggregator = AlertAggregator()
    print("Alert aggregator ready")
