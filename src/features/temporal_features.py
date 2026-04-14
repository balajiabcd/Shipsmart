import pandas as pd
import numpy as np
from typing import Optional, List


def create_temporal_features(
    df: pd.DataFrame, datetime_col: str = "order_time", drop_original: bool = False
) -> pd.DataFrame:
    """Create temporal features from datetime column.

    Args:
        df: Input dataframe
        datetime_col: Name of datetime column to extract features from
        drop_original: Whether to drop the original datetime column

    Returns:
        DataFrame with temporal features
    """
    df = df.copy()
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors="coerce")

    features = pd.DataFrame(index=df.index)

    features["hour"] = df[datetime_col].dt.hour
    features["day_of_week"] = df[datetime_col].dt.dayofweek
    features["day_of_month"] = df[datetime_col].dt.day
    features["week_of_year"] = df[datetime_col].dt.isocalendar().week.astype(int)
    features["month"] = df[datetime_col].dt.month
    features["quarter"] = df[datetime_col].dt.quarter
    features["year"] = df[datetime_col].dt.year
    features["day_of_year"] = df[datetime_col].dt.dayofyear

    features["is_weekend"] = (features["day_of_week"] >= 5).astype(int)
    features["is_business_hour"] = (
        (features["hour"] >= 9) & (features["hour"] <= 17)
    ).astype(int)
    features["is_morning_rush"] = (
        (features["hour"] >= 7) & (features["hour"] <= 9)
    ).astype(int)
    features["is_evening_rush"] = (
        (features["hour"] >= 16) & (features["hour"] <= 19)
    ).astype(int)
    features["is_night"] = ((features["hour"] >= 22) | (features["hour"] <= 5)).astype(
        int
    )

    features["time_period"] = pd.cut(
        features["hour"],
        bins=[-1, 6, 12, 18, 24],
        labels=["night", "morning", "afternoon", "evening"],
    ).astype(str)

    features["is_month_start"] = df[datetime_col].dt.is_month_start.astype(int)
    features["is_month_end"] = df[datetime_col].dt.is_month_end.astype(int)
    features["is_quarter_start"] = df[datetime_col].dt.is_quarter_start.astype(int)
    features["is_quarter_end"] = df[datetime_col].dt.is_quarter_end.astype(int)

    if drop_original:
        features[datetime_col] = df[datetime_col]

    return features


def add_temporal_features_to_df(
    df: pd.DataFrame, datetime_col: str = "order_time"
) -> pd.DataFrame:
    """Add temporal features directly to the dataframe.

    Args:
        df: Input dataframe
        datetime_col: Name of datetime column

    Returns:
        DataFrame with additional temporal features
    """
    temporal = create_temporal_features(df, datetime_col)
    result = pd.concat([df, temporal], axis=1)
    return result


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        orders = pd.read_csv("data/raw/orders.csv")
        temporal = create_temporal_features(orders)
        temporal.to_csv("data/features/temporal_features.csv", index=False)
        print(f"Created temporal features: {temporal.shape}")
        print(f"Columns: {list(temporal.columns)}")
    except Exception as e:
        print(f"Error: {e}")
