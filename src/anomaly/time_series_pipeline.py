import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


class TimeSeriesPipeline:
    def __init__(self):
        self.data = None
        self.features = None

    def load_delivery_data(
        self, start_date: datetime, end_date: datetime, file_path: str = None
    ) -> pd.DataFrame:
        if file_path is None:
            file_path = "data/simulated/delivery_events.csv"

        try:
            df = pd.read_csv(file_path)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]
            self.data = df
            return df
        except FileNotFoundError:
            return self._generate_sample_data(start_date, end_date)

    def _generate_sample_data(
        self, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        dates = pd.date_range(start_date, end_date, freq="H")
        n = len(dates)

        df = pd.DataFrame(
            {
                "timestamp": dates,
                "delivery_id": [f"DEL{i:04d}" for i in range(n)],
                "delay_minutes": np.random.exponential(15, n),
                "is_delayed": np.random.choice([0, 1], n, p=[0.7, 0.3]),
                "driver_id": [f"DRV{np.random.randint(1, 20):03d}" for _ in range(n)],
            }
        )

        self.data = df
        return df

    def aggregate_metrics(self, df: pd.DataFrame, freq: str = "H") -> pd.DataFrame:
        if "timestamp" not in df.columns:
            return pd.DataFrame()

        df = df.set_index("timestamp")

        metrics = pd.DataFrame()

        if "delivery_id" in df.columns:
            metrics["delivery_count"] = df.resample(freq).size()

        if "delay_minutes" in df.columns:
            metrics["avg_delay"] = df["delay_minutes"].resample(freq).mean()

        if "is_delayed" in df.columns:
            metrics["delay_rate"] = df["is_delayed"].resample(freq).mean()

        if "driver_id" in df.columns:
            metrics["driver_count"] = df["driver_id"].resample(freq).nunique()

        self.features = metrics.fillna(0)
        return self.features

    def create_lag_features(
        self, df: pd.DataFrame, lags: List[int] = None
    ) -> pd.DataFrame:
        if lags is None:
            lags = [1, 2, 4, 8, 24]

        if "delay_rate" not in df.columns:
            if "is_delayed" in df.columns:
                df["delay_rate"] = df["is_delayed"]
            else:
                return df

        for lag in lags:
            df[f"lag_{lag}h"] = df["delay_rate"].shift(lag)

        if "delay_rate" in df.columns:
            df["rolling_mean_4h"] = df["delay_rate"].rolling(window=4).mean()
            df["rolling_std_4h"] = df["delay_rate"].rolling(window=4).std()
            df["rolling_mean_24h"] = df["delay_rate"].rolling(window=24).mean()

        return df.dropna()

    def prepare_for_detection(
        self, df: pd.DataFrame, target_column: str = "delay_rate"
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if target_column not in df.columns:
            return pd.DataFrame(), pd.DataFrame()

        X = df.drop(columns=[target_column])
        y = df[target_column]

        return X, y

    def get_rolling_statistics(
        self, df: pd.DataFrame, window: int = 24
    ) -> pd.DataFrame:
        result = pd.DataFrame()

        for col in ["delivery_count", "avg_delay", "delay_rate"]:
            if col in df.columns:
                result[f"{col}_rolling_mean"] = df[col].rolling(window).mean()
                result[f"{col}_rolling_std"] = df[col].rolling(window).std()

        return result.fillna(0)


if __name__ == "__main__":
    pipeline = TimeSeriesPipeline()
    print("Time series pipeline ready")
