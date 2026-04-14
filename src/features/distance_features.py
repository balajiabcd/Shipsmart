import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from typing import Tuple, Optional


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in km using Haversine formula."""
    R = 6371

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def create_distance_features(
    df: pd.DataFrame,
    origin_lat_col: str = "origin_lat",
    origin_lon_col: str = "origin_lon",
    dest_lat_col: str = "dest_lat",
    dest_lon_col: str = "dest_lon",
) -> pd.DataFrame:
    """Create distance features from origin and destination coordinates.

    Args:
        df: Input dataframe with latitude/longitude columns
        origin_lat_col: Column name for origin latitude
        origin_lon_col: Column name for origin longitude
        dest_lat_col: Column name for destination latitude
        dest_lon_col: Column name for destination longitude

    Returns:
        DataFrame with distance features
    """
    features = pd.DataFrame(index=df.index)

    features["distance_km"] = df.apply(
        lambda row: (
            haversine(
                row[origin_lat_col],
                row[origin_lon_col],
                row[dest_lat_col],
                row[dest_lon_col],
            )
            if pd.notna(row[origin_lat_col]) and pd.notna(row[dest_lat_col])
            else np.nan
        ),
        axis=1,
    )

    features["distance_bucket"] = pd.cut(
        features["distance_km"],
        bins=[-1, 50, 100, 200, 500, float("inf")],
        labels=["short", "medium", "long", "very_long", "extra_long"],
    )

    features["lat_diff"] = df[dest_lat_col] - df[origin_lat_col]
    features["lon_diff"] = df[dest_lon_col] - df[origin_lon_col]

    features["is_long_distance"] = (features["distance_km"] > 200).astype(int)
    features["is_short_distance"] = (features["distance_km"] <= 50).astype(int)

    features["direction_angle"] = np.degrees(
        np.arctan2(features["lon_diff"], features["lat_diff"])
    )

    features["euclidean_distance"] = np.sqrt(
        features["lat_diff"] ** 2 + features["lon_diff"] ** 2
    )

    features["distance_ratio"] = features["distance_km"] / (
        features["euclidean_distance"] + 0.001
    )

    return features


def calculate_distance_matrix(coords: list) -> np.ndarray:
    """Calculate pairwise distance matrix for a list of coordinates.

    Args:
        coords: List of (lat, lon) tuples

    Returns:
        Distance matrix
    """
    n = len(coords)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i, j] = haversine(
                    coords[i][0], coords[i][1], coords[j][0], coords[j][1]
                )

    return matrix


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        orders = pd.read_csv("data/raw/orders.csv")

        required_cols = ["origin_lat", "origin_lon", "dest_lat", "dest_lon"]
        if all(col in orders.columns for col in required_cols):
            dist_features = create_distance_features(orders)
            dist_features.to_csv("data/features/distance_features.csv", index=False)
            print(f"Created distance features: {dist_features.shape}")
            print(f"Columns: {list(dist_features.columns)}")
        else:
            print(f"Missing columns. Available: {list(orders.columns)}")
    except Exception as e:
        print(f"Error: {e}")
