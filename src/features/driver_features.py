import pandas as pd
import numpy as np
from typing import Optional


def create_driver_scores(
    df: pd.DataFrame,
    driver_id_col: str = "driver_id",
    on_time_col: str = "on_time_deliveries",
    total_col: str = "total_deliveries",
    rating_col: str = "rating",
    delay_col: str = "avg_delay_minutes",
) -> pd.DataFrame:
    """Create driver performance scores from historical data.

    Args:
        df: Input dataframe with driver performance data
        driver_id_col: Driver identifier column
        on_time_col: On-time deliveries column
        total_col: Total deliveries column
        rating_col: Rating column
        delay_col: Average delay column

    Returns:
        DataFrame with driver performance features
    """
    features = pd.DataFrame()

    if on_time_col in df.columns and total_col in df.columns:

        def calc_on_time_rate(group):
            on_time = group[on_time_col].sum()
            total = group[total_col].sum()
            return (on_time / total * 100) if total > 0 else 0

        features["on_time_rate"] = (
            df.groupby(driver_id_col).apply(calc_on_time_rate).values
        )

        total_by_driver = df.groupby(driver_id_col)[total_col].sum()
        features["total_deliveries"] = (
            df.groupby(driver_id_col)[total_col].sum().reindex(features.index).values
        )
    else:
        features["on_time_rate"] = 80.0
        features["total_deliveries"] = 0

    if rating_col in df.columns:
        features["avg_rating"] = (
            df.groupby(driver_id_col)[rating_col].mean().reindex(features.index).values
        )
        features["min_rating"] = (
            df.groupby(driver_id_col)[rating_col].min().reindex(features.index).values
        )
        features["max_rating"] = (
            df.groupby(driver_id_col)[rating_col].max().reindex(features.index).values
        )
    else:
        features["avg_rating"] = 4.0
        features["min_rating"] = 4.0
        features["max_rating"] = 4.0

    if delay_col in df.columns:
        features["avg_delay"] = (
            df.groupby(driver_id_col)[delay_col].mean().reindex(features.index).values
        )
    else:
        features["avg_delay"] = 10.0

    features["driver_id"] = features.index

    features["performance_score"] = (
        features["on_time_rate"] * 0.4
        + features["avg_rating"] * 20 * 0.35
        + (100 - np.minimum(features["avg_delay"], 100)) * 0.25
    )

    features["performance_level"] = pd.cut(
        features["performance_score"],
        bins=[-1, 60, 75, 85, 100],
        labels=["poor", "average", "good", "excellent"],
    ).astype(str)

    features["is_top_performer"] = (features["performance_score"] >= 85).astype(int)
    features["is_poor_performer"] = (features["performance_score"] <= 60).astype(int)

    return features.reset_index(drop=True)


def create_driver_risk_score(
    df: pd.DataFrame,
    driver_id_col: str = "driver_id",
    rating_col: str = "rating",
    delay_col: str = "avg_delay_minutes",
) -> pd.DataFrame:
    """Create driver risk score based on performance metrics."""
    features = pd.DataFrame()

    features["driver_id"] = df[driver_id_col].unique()

    avg_rating = df.groupby(driver_id_col)[rating_col].mean()
    avg_delay = (
        df.groupby(driver_id_col)[delay_col].mean()
        if delay_col in df.columns
        else pd.Series(0)
    )

    features["rating_risk"] = features["driver_id"].map(
        lambda x: max(0, 5 - avg_rating.get(x, 5)) * 20
    )

    features["delay_risk"] = features["driver_id"].map(
        lambda x: min(100, avg_delay.get(x, 0))
    )

    features["total_risk_score"] = (
        features["rating_risk"] * 0.5 + features["delay_risk"] * 0.5
    )

    features["risk_level"] = pd.cut(
        features["total_risk_score"],
        bins=[-1, 20, 40, 60, 100],
        labels=["low", "medium", "high", "critical"],
    ).astype(str)

    return features


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        drivers_perf = pd.read_csv("data/raw/drivers_performance.csv")
        driver_features = create_driver_scores(drivers_perf)
        driver_features.to_csv("data/features/driver_scores.csv", index=False)
        print(f"Created driver features: {driver_features.shape}")
        print(f"Columns: {list(driver_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
