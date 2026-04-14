import numpy as np
import pandas as pd
from typing import List, Tuple, Dict


class StatisticalAnomalyDetector:
    def __init__(self, z_threshold: float = 3.0, iqr_factor: float = 1.5):
        self.z_threshold = z_threshold
        self.iqr_factor = iqr_factor
        self.baseline_stats: Dict = {}

    def fit(self, data: pd.Series):
        self.baseline_stats = {
            "mean": float(data.mean()),
            "std": float(data.std()),
            "q1": float(data.quantile(0.25)),
            "q3": float(data.quantile(0.75)),
            "median": float(data.median()),
        }
        self.baseline_stats["iqr"] = (
            self.baseline_stats["q3"] - self.baseline_stats["q1"]
        )

    def detect_zscore(self, data: pd.Series) -> pd.Series:
        if not self.baseline_stats:
            self.fit(data)

        if self.baseline_stats["std"] == 0:
            return pd.Series([False] * len(data), index=data.index)

        z_scores = (data - self.baseline_stats["mean"]) / self.baseline_stats["std"]
        return abs(z_scores) > self.z_threshold

    def detect_iqr(self, data: pd.Series) -> pd.Series:
        if not self.baseline_stats:
            self.fit(data)

        q1 = self.baseline_stats["q1"]
        q3 = self.baseline_stats["q3"]
        iqr = self.baseline_stats["iqr"]

        lower = q1 - self.iqr_factor * iqr
        upper = q3 + self.iqr_factor * iqr

        return (data < lower) | (data > upper)

    def detect(self, data: pd.Series, method: str = "zscore") -> pd.Series:
        if method == "zscore":
            return self.detect_zscore(data)
        elif method == "iqr":
            return self.detect_iqr(data)
        elif method == "both":
            return self.detect_zscore(data) | self.detect_iqr(data)
        else:
            raise ValueError(f"Unknown method: {method}")

    def get_anomaly_scores(self, data: pd.Series) -> pd.Series:
        if not self.baseline_stats:
            self.fit(data)

        if self.baseline_stats["std"] == 0:
            return pd.Series([0.0] * len(data), index=data.index)

        return abs((data - self.baseline_stats["mean"]) / self.baseline_stats["std"])

    def fit_detect(
        self, data: pd.Series, method: str = "zscore"
    ) -> Tuple[pd.Series, pd.Series]:
        self.fit(data)
        return self.detect(data, method)

    def get_anomalies(self, data: pd.Series, method: str = "zscore") -> List[int]:
        anomalies = self.detect(data, method)
        return list(anomalies[anomalies].index)


if __name__ == "__main__":
    detector = StatisticalAnomalyDetector()
    print("Statistical anomaly detector ready")
