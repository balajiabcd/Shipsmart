import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict


def get_german_holidays() -> Dict[str, List[str]]:
    """Get German public holidays by year."""
    holidays = {
        2024: [
            "2024-01-01",
            "2024-03-29",
            "2024-04-01",
            "2024-05-01",
            "2024-05-09",
            "2024-05-20",
            "2024-10-03",
            "2024-12-25",
            "2024-12-26",
        ],
        2025: [
            "2025-01-01",
            "2025-04-18",
            "2025-04-21",
            "2025-05-01",
            "2025-05-29",
            "2025-06-09",
            "2025-10-03",
            "2025-12-25",
            "2025-12-26",
        ],
        2026: [
            "2026-01-01",
            "2026-04-03",
            "2026-04-06",
            "2026-05-01",
            "2026-05-21",
            "2026-06-01",
            "2026-10-03",
            "2026-12-25",
            "2026-12-26",
        ],
    }
    return holidays


def create_holiday_features(
    df: pd.DataFrame,
    datetime_col: str = "order_time",
    holidays_dict: Optional[Dict[str, List[str]]] = None,
) -> pd.DataFrame:
    """Create holiday-related features.

    Args:
        df: Input dataframe
        datetime_col: Datetime column name
        holidays_dict: Dictionary of holidays by year

    Returns:
        DataFrame with holiday features
    """
    if holidays_dict is None:
        holidays_dict = get_german_holidays()

    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors="coerce")

    features = pd.DataFrame(index=df_copy.index)

    dates = df_copy[datetime_col].dt.date

    all_holidays = []
    for year_holidays in holidays_dict.values():
        all_holidays.extend(
            [datetime.strptime(d, "%Y-%m-%d").date() for d in year_holidays]
        )

    features["is_holiday"] = dates.isin(all_holidays).astype(int)

    def days_to_nearest_holiday(date):
        if pd.isna(date):
            return 30
        min_distance = 365
        for holiday in all_holidays:
            distance = abs((date - holiday).days)
            min_distance = min(min_distance, distance)
        return min_distance

    features["days_to_holiday"] = dates.apply(days_to_nearest_holiday)

    features["is_holiday_week"] = (features["days_to_holiday"] <= 7).astype(int)
    features["is_holiday_month"] = (features["days_to_holiday"] <= 30).astype(int)

    def is_pre_holiday(date):
        if pd.isna(date):
            return 0
        for holiday in all_holidays:
            if 1 <= (holiday - date).days <= 3:
                return 1
        return 0

    features["is_pre_holiday"] = dates.apply(is_pre_holiday)

    def is_post_holiday(date):
        if pd.isna(date):
            return 0
        for holiday in all_holidays:
            if 1 <= (date - holiday).days <= 3:
                return 1
        return 0

    features["is_post_holiday"] = dates.apply(is_post_holiday)

    features["holiday_period"] = pd.cut(
        features["days_to_holiday"],
        bins=[-1, 3, 7, 30, 365],
        labels=["on_holiday", "near_holiday", "upcoming_holiday", "normal"],
    ).astype(str)

    return features


def add_holiday_calendar(
    df: pd.DataFrame, datetime_col: str = "order_time"
) -> pd.DataFrame:
    """Add German holiday calendar info."""
    holidays_dict = get_german_holidays()
    return create_holiday_features(df, datetime_col, holidays_dict)


def create_holiday_name_features(
    df: pd.DataFrame, datetime_col: str = "order_time"
) -> pd.DataFrame:
    """Create features with specific holiday names."""
    holidays_dict = get_german_holidays()

    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors="coerce")

    features = pd.DataFrame(index=df_copy.index)

    holiday_map = {}
    for year, dates in holidays_dict.items():
        for d in dates:
            date = datetime.strptime(d, "%Y-%m-%d").date()
            if date.month == 12 and date.day == 25:
                holiday_map[date] = "christmas"
            elif date.month == 12 and date.day == 31:
                holiday_map[date] = "new_years_eve"
            elif date.month == 1 and date.day == 1:
                holiday_map[date] = "new_year"
            elif date.month == 5 and date.day == 1:
                holiday_map[date] = "labor_day"
            elif date.month == 10 and date.day == 3:
                holiday_map[date] = "german_unity"
            elif date.month == 4 or date.month == 3:
                holiday_map[date] = "easter"
            else:
                holiday_map[date] = "other_holiday"

    dates = df_copy[datetime_col].dt.date
    features["holiday_name"] = dates.map(lambda x: holiday_map.get(x, "none"))

    return features


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        orders = pd.read_csv("data/raw/orders.csv")
        holiday_features = create_holiday_features(orders)
        holiday_features.to_csv("data/features/holiday_features.csv", index=False)
        print(f"Created holiday features: {holiday_features.shape}")
        print(f"Columns: {list(holiday_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
