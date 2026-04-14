import pandas as pd
import numpy as np
from typing import Optional, List


HOLIDAY_SEASON_MONTHS = [11, 12]
SUMMER_MONTHS = [6, 7, 8]
PEAK_SHOPPING_MONTHS = [11, 12]
LOW_SEASON_MONTHS = [1, 2]


def create_seasonality_features(
    df: pd.DataFrame, datetime_col: str = "order_time"
) -> pd.DataFrame:
    """Create demand seasonality features from datetime.

    Args:
        df: Input dataframe
        datetime_col: Datetime column name

    Returns:
        DataFrame with seasonality features
    """
    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors="coerce")

    features = pd.DataFrame(index=df_copy.index)

    features["month"] = df_copy[datetime_col].dt.month
    features["quarter"] = df_copy[datetime_col].dt.quarter
    features["week_of_year"] = df_copy[datetime_col].dt.isocalendar().week.astype(int)
    features["day_of_year"] = df_copy[datetime_col].dt.dayofyear

    features["is_holiday_season"] = (
        features["month"].isin(HOLIDAY_SEASON_MONTHS).astype(int)
    )
    features["is_summer"] = features["month"].isin(SUMMER_MONTHS).astype(int)
    features["is_peak_shopping"] = (
        features["month"].isin(PEAK_SHOPPING_MONTHS).astype(int)
    )
    features["is_low_season"] = features["month"].isin(LOW_SEASON_MONTHS).astype(int)

    features["is_month_start"] = df_copy[datetime_col].dt.is_month_start.astype(int)
    features["is_month_mid"] = (
        (df_copy[datetime_col].dt.day >= 10) & (df_copy[datetime_col].dt.day <= 20)
    ).astype(int)
    features["is_month_end"] = df_copy[datetime_col].dt.is_month_end.astype(int)

    features["is_quarter_start"] = df_copy[datetime_col].dt.is_quarter_start.astype(int)
    features["is_quarter_end"] = df_copy[datetime_col].dt.is_quarter_end.astype(int)

    features["season"] = features["month"].map(
        lambda x: (
            "winter"
            if x in [12, 1, 2]
            else "spring"
            if x in [3, 4, 5]
            else "summer"
            if x in [6, 7, 8]
            else "fall"
        )
    )

    demand_level_map = {
        1: 0.6,
        2: 0.6,
        3: 0.8,
        4: 0.8,
        5: 0.9,
        6: 1.0,
        7: 0.9,
        8: 0.9,
        9: 0.8,
        10: 1.0,
        11: 1.3,
        12: 1.5,
    }
    features["seasonal_demand_factor"] = features["month"].map(demand_level_map)

    features["is_holiday"] = (features["month"] == 12).astype(int)
    features["is_new_year"] = (
        (features["month"] == 1) & (df_copy[datetime_col].dt.day <= 7)
    ).astype(int)

    return features


def create_lag_features(
    df: pd.DataFrame, value_col: str, lags: List[int] = [1, 7, 14, 30]
) -> pd.DataFrame:
    """Create lag features for time series.

    Args:
        df: Input dataframe
        value_col: Column to create lags for
        lags: List of lag periods

    Returns:
        DataFrame with lag features
    """
    features = pd.DataFrame(index=df.index)

    for lag in lags:
        features[f"{value_col}_lag_{lag}"] = df[value_col].shift(lag)

    return features


def create_rolling_features(
    df: pd.DataFrame, value_col: str, windows: List[int] = [7, 14, 30]
) -> pd.DataFrame:
    """Create rolling window features.

    Args:
        df: Input dataframe
        value_col: Column to create rolling features for
        windows: List of window sizes

    Returns:
        DataFrame with rolling features
    """
    features = pd.DataFrame(index=df.index)

    for window in windows:
        features[f"{value_col}_rolling_mean_{window}"] = (
            df[value_col].rolling(window=window, min_periods=1).mean()
        )
        features[f"{value_col}_rolling_std_{window}"] = (
            df[value_col].rolling(window=window, min_periods=1).std()
        )

    return features


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        orders = pd.read_csv("data/raw/orders.csv")
        seasonality = create_seasonality_features(orders)
        seasonality.to_csv("data/features/seasonality_features.csv", index=False)
        print(f"Created seasonality features: {seasonality.shape}")
        print(f"Columns: {list(seasonality.columns)}")
    except Exception as e:
        print(f"Error: {e}")
