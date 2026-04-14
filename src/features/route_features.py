import pandas as pd
import numpy as np
from typing import Optional


ROUTE_TYPE_COMPLEXITY = {
    "highway": 1,
    "primary": 2,
    "secondary": 3,
    "tertiary": 4,
    "residential": 5,
    "local": 4,
}


def create_route_complexity(
    df: pd.DataFrame,
    route_id_col: str = "route_id",
    distance_col: str = "distance_km",
    route_type_col: str = "route_type",
    num_stops_col: Optional[str] = "num_stops",
    avg_speed_col: Optional[str] = "avg_speed_kmh",
) -> pd.DataFrame:
    """Create route complexity features.

    Args:
        df: Input dataframe with route data
        route_id_col: Route identifier column
        distance_col: Distance column
        route_type_col: Route type column
        num_stops_col: Number of stops column (optional)
        avg_speed_col: Average speed column (optional)

    Returns:
        DataFrame with route complexity features
    """
    features = pd.DataFrame(index=df.index)

    if distance_col in df.columns:
        features["distance_km"] = df[distance_col]
        features["distance_factor"] = (
            pd.cut(
                df[distance_col],
                bins=[0, 50, 100, 200, 500, float("inf")],
                labels=[1, 2, 3, 4, 5],
            )
            .astype(float)
            .fillna(2)
        )
    else:
        features["distance_km"] = 50
        features["distance_factor"] = 2

    if route_type_col in df.columns:
        features["route_type_complexity"] = (
            df[route_type_col].map(ROUTE_TYPE_COMPLEXITY).fillna(3)
        )
    else:
        features["route_type_complexity"] = 3

    if num_stops_col in df.columns:
        features["num_stops"] = df[num_stops_col]
        features["stops_factor"] = (
            pd.cut(
                df[num_stops_col],
                bins=[-1, 2, 5, 10, 20, float("inf")],
                labels=[1, 2, 3, 4, 5],
            )
            .astype(float)
            .fillna(2)
        )
    else:
        features["num_stops"] = 3
        features["stops_factor"] = 2

    if avg_speed_col in df.columns:
        features["avg_speed"] = df[avg_speed_col]
        features["speed_factor"] = (
            pd.cut(
                df[avg_speed_col],
                bins=[0, 30, 50, 70, 100, float("inf")],
                labels=[5, 4, 3, 2, 1],
            )
            .astype(float)
            .fillna(3)
        )
    else:
        features["avg_speed"] = 50
        features["speed_factor"] = 3

    features["route_complexity_index"] = (
        features["distance_factor"] * 0.3
        + features["route_type_complexity"] * 0.25
        + features["stops_factor"] * 0.25
        + features["speed_factor"] * 0.2
    )

    features["complexity_level"] = pd.cut(
        features["route_complexity_index"],
        bins=[-1, 2, 3, 4, 10],
        labels=["simple", "moderate", "complex", "very_complex"],
    ).astype(str)

    features["is_complex_route"] = (features["route_complexity_index"] >= 3.5).astype(
        int
    )
    features["is_simple_route"] = (features["route_complexity_index"] <= 2).astype(int)

    return features


def create_route_difficulty_score(df: pd.DataFrame) -> pd.DataFrame:
    """Create route difficulty score with weather/traffic considerations."""
    features = create_route_complexity(df)

    features["difficulty_score"] = (
        features["route_complexity_index"] * 0.6 + features["stops_factor"] * 0.4
    )

    features["difficulty_level"] = pd.cut(
        features["difficulty_score"],
        bins=[-1, 2, 3, 4, 10],
        labels=["easy", "moderate", "hard", "expert"],
    ).astype(str)

    return features


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        routes = pd.read_csv("data/raw/routes.csv")
        route_features = create_route_complexity(routes)
        route_features.to_csv("data/features/route_complexity.csv", index=False)
        print(f"Created route complexity features: {route_features.shape}")
        print(f"Columns: {list(route_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
