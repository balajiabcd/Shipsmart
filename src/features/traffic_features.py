import pandas as pd
import numpy as np
from typing import Optional, List


def calculate_congestion_level(congestion_str: str) -> int:
    """Convert congestion string to numeric level."""
    if pd.isna(congestion_str):
        return 0

    mapping = {"low": 1, "medium": 2, "high": 3, "very_high": 4, "severe": 5}
    return mapping.get(str(congestion_str).lower(), 0)


def create_traffic_index(
    df: pd.DataFrame,
    route_id_col: str = "route_id",
    congestion_col: str = "congestion_level",
    hour_col: Optional[str] = "hour",
) -> pd.DataFrame:
    """Create traffic index features from traffic data.

    Args:
        df: Input dataframe with traffic data
        route_id_col: Route identifier column
        congestion_col: Congestion level column
        hour_col: Hour column (optional)

    Returns:
        DataFrame with traffic index features
    """
    features = pd.DataFrame(index=df.index)

    if congestion_col in df.columns:
        if df[congestion_col].dtype == object:
            features["congestion_numeric"] = df[congestion_col].apply(
                calculate_congestion_level
            )
        else:
            features["congestion_numeric"] = df[congestion_col]

        features["avg_congestion_by_route"] = df.groupby(route_id_col)[
            congestion_col
        ].transform("mean")
        features["congestion_vs_route_avg"] = (
            features["congestion_numeric"] - features["avg_congestion_by_route"]
        )
    else:
        features["congestion_numeric"] = 0
        features["avg_congestion_by_route"] = 0
        features["congestion_vs_route_avg"] = 0

    if hour_col and hour_col in df.columns:
        features["hour"] = df[hour_col]

        peak_morning = (df[hour_col] >= 7) & (df[hour_col] <= 9)
        peak_evening = (df[hour_col] >= 16) & (df[hour_col] <= 19)

        features["is_peak_hour"] = (peak_morning | peak_evening).astype(int)
        features["is_morning_peak"] = peak_morning.astype(int)
        features["is_evening_peak"] = peak_evening.astype(int)

        features["rush_hour_index"] = features["congestion_numeric"] * (
            1 + 0.5 * features["is_peak_hour"]
        )
    else:
        features["is_peak_hour"] = 0
        features["is_morning_peak"] = 0
        features["is_evening_peak"] = 0
        features["rush_hour_index"] = features["congestion_numeric"]

    features["traffic_index"] = features["congestion_numeric"] * features.get(
        "avg_congestion_by_route", 1
    )

    features["traffic_level"] = pd.cut(
        features["traffic_index"],
        bins=[-1, 2, 4, 6, 100],
        labels=["light", "moderate", "heavy", "severe"],
    ).astype(str)

    features["is_high_traffic"] = (features["traffic_index"] >= 4).astype(int)
    features["is_severe_traffic"] = (features["traffic_index"] >= 6).astype(int)

    return features


def create_route_traffic_summary(
    df: pd.DataFrame, route_id_col: str = "route_id"
) -> pd.DataFrame:
    """Create aggregated traffic summary per route."""
    summary = (
        df.groupby(route_id_col)
        .agg(
            {
                "congestion_level": ["mean", "max", "std"],
            }
        )
        .reset_index()
    )

    summary.columns = [
        route_id_col,
        "avg_congestion",
        "max_congestion",
        "std_congestion",
    ]
    summary["std_congestion"] = summary["std_congestion"].fillna(0)

    return summary


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        traffic = pd.read_csv("data/raw/traffic.csv")
        traffic_features = create_traffic_index(traffic)
        traffic_features.to_csv("data/features/traffic_features.csv", index=False)
        print(f"Created traffic features: {traffic_features.shape}")
        print(f"Columns: {list(traffic_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
