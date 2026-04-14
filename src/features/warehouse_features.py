import pandas as pd
import numpy as np
from typing import Optional


def create_warehouse_scores(
    df: pd.DataFrame,
    warehouse_id_col: str = "warehouse_id",
    throughput_col: str = "daily_throughput",
    processing_time_col: str = "avg_processing_time_minutes",
    delay_rate_col: str = "delay_rate_percent",
    utilization_col: str = "utilization_percent",
) -> pd.DataFrame:
    """Create warehouse efficiency scores from performance data.

    Args:
        df: Input dataframe with warehouse performance data
        warehouse_id_col: Warehouse identifier column
        throughput_col: Daily throughput column
        processing_time_col: Processing time column
        delay_rate_col: Delay rate column
        utilization_col: Utilization column

    Returns:
        DataFrame with warehouse efficiency features
    """
    features = pd.DataFrame()

    if throughput_col in df.columns:
        features["avg_throughput"] = (
            df.groupby(warehouse_id_col)[throughput_col]
            .mean()
            .reindex(features.index if len(features) > 0 else None)
            .values
        )
        features["max_throughput"] = (
            df.groupby(warehouse_id_col)[throughput_col]
            .max()
            .reindex(features.index if len(features) > 0 else None)
            .values
        )
    else:
        features["avg_throughput"] = 1000
        features["max_throughput"] = 1500

    if processing_time_col in df.columns:
        features["avg_processing_time"] = (
            df.groupby(warehouse_id_col)[processing_time_col]
            .mean()
            .reindex(features.index if len(features) > 0 else None)
            .values
        )
    else:
        features["avg_processing_time"] = 30

    if delay_rate_col in df.columns:
        features["avg_delay_rate"] = (
            df.groupby(warehouse_id_col)[delay_rate_col]
            .mean()
            .reindex(features.index if len(features) > 0 else None)
            .values
        )
    else:
        features["avg_delay_rate"] = 5.0

    if utilization_col in df.columns:
        features["avg_utilization"] = (
            df.groupby(warehouse_id_col)[utilization_col]
            .mean()
            .reindex(features.index if len(features) > 0 else None)
            .values
        )
        features["max_utilization"] = (
            df.groupby(warehouse_id_col)[utilization_col]
            .max()
            .reindex(features.index if len(features) > 0 else None)
            .values
        )
    else:
        features["avg_utilization"] = 70
        features["max_utilization"] = 90

    features["warehouse_id"] = features.index

    features["efficiency_score"] = (
        (100 - features["avg_delay_rate"]) * 0.35
        + (features["avg_utilization"] / 100) * 30
        + (1 / (features["avg_processing_time"] + 1)) * 35 * 100
    )

    features["efficiency_level"] = pd.cut(
        features["efficiency_score"],
        bins=[-1, 60, 75, 85, 100],
        labels=["low", "medium", "high", "excellent"],
    ).astype(str)

    features["is_bottleneck"] = (
        (features["avg_utilization"] > 85) | (features["avg_delay_rate"] > 10)
    ).astype(int)

    features["is_efficient"] = (features["efficiency_score"] >= 80).astype(int)

    return features.reset_index(drop=True)


def create_warehouse_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """Create warehouse risk score based on performance issues."""
    features = pd.DataFrame()

    if "warehouse_id" in df.columns:
        features["warehouse_id"] = df["warehouse_id"].unique()

        utilization_risk = (
            df.groupby("warehouse_id")["utilization_percent"].max()
            if "utilization_percent" in df.columns
            else pd.Series(0)
        )
        delay_risk = (
            df.groupby("warehouse_id")["delay_rate_percent"].mean()
            if "delay_rate_percent" in df.columns
            else pd.Series(0)
        )

        features["utilization_risk"] = features["warehouse_id"].map(
            lambda x: (
                min(100, utilization_risk.get(x, 0))
                if x in utilization_risk.index
                else 0
            )
        )

        features["delay_risk"] = features["warehouse_id"].map(
            lambda x: delay_risk.get(x, 0) if x in delay_risk.index else 0
        )

        features["total_risk_score"] = (
            features["utilization_risk"] * 0.5 + features["delay_risk"] * 0.5
        )
    else:
        features["warehouse_id"] = []
        features["utilization_risk"] = []
        features["delay_risk"] = []
        features["total_risk_score"] = []

    return features


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        warehouse_perf = pd.read_csv("data/raw/warehouse_performance.csv")
        warehouse_features = create_warehouse_scores(warehouse_perf)
        warehouse_features.to_csv("data/features/warehouse_scores.csv", index=False)
        print(f"Created warehouse features: {warehouse_features.shape}")
        print(f"Columns: {list(warehouse_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
