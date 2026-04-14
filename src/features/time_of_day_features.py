import pandas as pd
import numpy as np
from typing import Optional


def create_time_of_day_features(
    df: pd.DataFrame, datetime_col: str = "order_time"
) -> pd.DataFrame:
    """Create time-of-day features from datetime.

    Args:
        df: Input dataframe
        datetime_col: Datetime column name

    Returns:
        DataFrame with time-of-day features
    """
    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors="coerce")

    features = pd.DataFrame(index=df_copy.index)

    hour = df_copy[datetime_col].dt.hour

    features["hour"] = hour

    features["is_night"] = ((hour >= 22) | (hour <= 5)).astype(int)
    features["is_morning"] = ((hour >= 6) & (hour < 12)).astype(int)
    features["is_afternoon"] = ((hour >= 12) & (hour < 18)).astype(int)
    features["is_evening"] = ((hour >= 18) & (hour < 22)).astype(int)

    features["time_period"] = (
        pd.cut(
            hour,
            bins=[-1, 5, 11, 17, 21, 24],
            labels=["night", "morning", "afternoon", "evening", "night"],
        )
        .astype(str)
        .replace("nightnight", "night")
    )

    features["is_peak_delivery_morning"] = ((hour >= 10) & (hour <= 12)).astype(int)
    features["is_peak_delivery_evening"] = ((hour >= 18) & (hour <= 20)).astype(int)
    features["is_peak_delivery"] = (
        features["is_peak_delivery_morning"] | features["is_peak_delivery_evening"]
    ).astype(int)

    features["is_late_night"] = ((hour >= 0) & (hour <= 5)).astype(int)
    features["is_early_morning"] = ((hour >= 6) & (hour <= 8)).astype(int)
    features["is_midday"] = ((hour >= 11) & (hour <= 14)).astype(int)
    features["is_late_afternoon"] = ((hour >= 15) & (hour <= 17)).astype(int)

    features["delivery_urgency"] = pd.cut(
        hour, bins=[-1, 6, 9, 12, 15, 18, 21, 24], labels=[1, 3, 4, 3, 4, 5, 3]
    ).astype(float)

    return features


def create_hour_buckets(
    df: pd.DataFrame, datetime_col: str = "order_time"
) -> pd.DataFrame:
    """Create hourly bucket features."""
    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors="coerce")

    features = pd.DataFrame(index=df_copy.index)

    hour = df_copy[datetime_col].dt.hour

    features["hour_bucket_2h"] = pd.cut(
        hour,
        bins=[-1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
        labels=[
            "0-2",
            "2-4",
            "4-6",
            "6-8",
            "8-10",
            "10-12",
            "12-14",
            "14-16",
            "16-18",
            "18-20",
            "20-22",
            "22-24",
        ],
    ).astype(str)

    features["is_business_hours"] = ((hour >= 8) & (hour <= 18)).astype(int)
    features["is_non_business_hours"] = ((hour < 8) | (hour > 18)).astype(int)

    return features


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        orders = pd.read_csv("data/raw/orders.csv")
        time_features = create_time_of_day_features(orders)
        time_features.to_csv("data/features/time_of_day.csv", index=False)
        print(f"Created time-of-day features: {time_features.shape}")
        print(f"Columns: {list(time_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
