import pandas as pd
import numpy as np
from typing import Optional, Tuple


def create_target_variable(
    orders_df: pd.DataFrame, delay_threshold_minutes: float = 0.0
) -> pd.DataFrame:
    """Create target variables for ML models.

    Args:
        orders_df: Orders dataframe
        delay_threshold_minutes: Minimum minutes to consider as delayed

    Returns:
        DataFrame with target variables
    """
    df = orders_df.copy()

    if "delivery_promise" in df.columns and "actual_delivery_time" in df.columns:
        df["delivery_promise"] = pd.to_datetime(df["delivery_promise"], errors="coerce")
        df["actual_delivery_time"] = pd.to_datetime(
            df["actual_delivery_time"], errors="coerce"
        )

        delay_minutes = (
            df["actual_delivery_time"] - df["delivery_promise"]
        ).dt.total_seconds() / 60

        is_delayed = (delay_minutes > delay_threshold_minutes).astype(int)

        pending_statuses = ["pending", "in_transit", "processing", "scheduled"]
        is_known = (
            ~df["status"].isin(pending_statuses) if "status" in df.columns else True
        )

        is_delayed = np.where(is_known, is_delayed, -1)

        delay_minutes_actual = np.where(is_known, delay_minutes, np.nan)

        target_df = pd.DataFrame(
            {
                "order_id": df["order_id"],
                "is_delayed": is_delayed,
                "delay_minutes": delay_minutes.fillna(0),
                "delay_minutes_actual": delay_minutes_actual,
            }
        )

    elif "delay_minutes" in df.columns:
        target_df = pd.DataFrame(
            {
                "order_id": df["order_id"],
                "is_delayed": (df["delay_minutes"] > delay_threshold_minutes).astype(
                    int
                ),
                "delay_minutes": df["delay_minutes"].fillna(0),
                "delay_minutes_actual": df["delay_minutes"],
            }
        )
    else:
        raise ValueError(
            "Required columns not found: delivery_promise + actual_delivery_time OR delay_minutes"
        )

    return target_df


def create_classification_target(df: pd.DataFrame, threshold: float = 0.0) -> pd.Series:
    """Create binary classification target (delayed or not)."""
    if "delay_minutes" in df.columns:
        return (df["delay_minutes"] > threshold).astype(int)
    elif "actual_delivery_time" in df.columns and "delivery_promise" in df.columns:
        delay = (
            df["actual_delivery_time"] - df["delivery_promise"]
        ).dt.total_seconds() / 60
        return (delay > threshold).astype(int)
    else:
        raise ValueError("Required columns not found")


def create_regression_target(df: pd.DataFrame) -> pd.Series:
    """Create regression target (delay minutes)."""
    if "delay_minutes" in df.columns:
        return df["delay_minutes"].fillna(0)
    elif "actual_delivery_time" in df.columns and "delivery_promise" in df.columns:
        return (
            df["actual_delivery_time"] - df["delivery_promise"]
        ).dt.total_seconds() / 60
    else:
        raise ValueError("Required columns not found")


def get_target_distribution(target_df: pd.DataFrame) -> dict:
    """Get distribution statistics of target variable."""
    valid_targets = target_df[target_df["is_delayed"] != -1]

    return {
        "total_orders": len(target_df),
        "delivered_orders": len(valid_targets),
        "delayed_count": (valid_targets["is_delayed"] == 1).sum(),
        "on_time_count": (valid_targets["is_delayed"] == 0).sum(),
        "pending_count": (target_df["is_delayed"] == -1).sum(),
        "delay_rate": (valid_targets["is_delayed"] == 1).mean() * 100,
        "avg_delay_minutes": valid_targets[valid_targets["is_delayed"] == 1][
            "delay_minutes"
        ].mean(),
    }


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        orders = pd.read_csv("data/raw/orders.csv")
        targets = create_target_variable(orders)
        targets.to_csv("data/features/target.csv", index=False)

        dist = get_target_distribution(targets)
        print(f"Target distribution:")
        print(f"  Total orders: {dist['total_orders']}")
        print(f"  Delayed: {dist['delayed_count']} ({dist['delay_rate']:.1f}%)")
        print(f"  On time: {dist['on_time_count']}")
        print(f"  Pending: {dist['pending_count']}")
        print(f"  Avg delay (when delayed): {dist['avg_delay_minutes']:.1f} min")
    except Exception as e:
        print(f"Error: {e}")
