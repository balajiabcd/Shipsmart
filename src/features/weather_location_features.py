import pandas as pd
import numpy as np
from typing import Optional, Dict


REGION_MAPPING = {
    "Berlin": "Berlin",
    "Munich": "Bavaria",
    "Hamburg": "Hamburg",
    "Frankfurt": "Hesse",
    "Cologne": "North Rhine-Westphalia",
    "Stuttgart": "Baden-Wurttemberg",
    "Dusseldorf": "North Rhine-Westphalia",
    "Dortmund": "North Rhine-Westphalia",
    "Essen": "North Rhine-Westphalia",
    "Leipzig": "Saxony",
}


WEATHER_RISK_BY_REGION = {
    "Berlin": 0.5,
    "Bavaria": 0.7,
    "Hamburg": 0.6,
    "Hesse": 0.5,
    "North Rhine-Westphalia": 0.5,
    "Baden-Wurttemberg": 0.6,
    "Saxony": 0.5,
}


def create_weather_location_features(
    weather_df: pd.DataFrame,
    location_df: Optional[pd.DataFrame] = None,
    location_col: str = "location_city",
    region_col: Optional[str] = None,
) -> pd.DataFrame:
    """Create weather-location combined features.

    Args:
        weather_df: Weather dataframe
        location_df: Location dataframe (optional)
        location_col: Location column name
        region_col: Region column name (optional)

    Returns:
        DataFrame with weather-location features
    """
    features = pd.DataFrame(index=weather_df.index)

    if location_col in weather_df.columns:
        features["location"] = weather_df[location_col]

        features["region"] = (
            weather_df[location_col].map(REGION_MAPPING).fillna("Other")
        )

        features["region_weather_risk"] = (
            features["region"].map(WEATHER_RISK_BY_REGION).fillna(0.5)
        )

        if "temperature_celsius" in weather_df.columns:
            temp_by_location = weather_df.groupby(location_col)[
                "temperature_celsius"
            ].mean()
            features["location_avg_temp"] = weather_df[location_col].map(
                temp_by_location
            )
            features["temp_diff_from_avg"] = (
                weather_df["temperature_celsius"] - features["location_avg_temp"]
            )

        if "condition" in weather_df.columns:
            condition_by_location = weather_df.groupby(location_col)["condition"].agg(
                lambda x: x.value_counts().index[0] if len(x) > 0 else "clear"
            )
            features["location_main_condition"] = weather_df[location_col].map(
                condition_by_location
            )

        if "wind_speed_kmh" in weather_df.columns:
            wind_by_location = weather_df.groupby(location_col)["wind_speed_kmh"].mean()
            features["location_avg_wind"] = weather_df[location_col].map(
                wind_by_location
            )
            features["wind_diff_from_avg"] = (
                weather_df["wind_speed_kmh"] - features["location_avg_wind"]
            )

        features["location_count"] = weather_df.groupby(location_col)[
            location_col
        ].transform("count")

    else:
        features["location"] = "Unknown"
        features["region"] = "Other"
        features["region_weather_risk"] = 0.5

    features["is_high_risk_region"] = (features["region_weather_risk"] >= 0.6).astype(
        int
    )

    features["weather_location_risk"] = features["region_weather_risk"]
    if "temperature_celsius" in weather_df.columns:
        temp_risk = np.where(
            (weather_df["temperature_celsius"] < 0)
            | (weather_df["temperature_celsius"] > 35),
            0.3,
            0,
        )
        features["weather_location_risk"] += temp_risk

    return features


def create_location_weather_profile(
    df: pd.DataFrame, location_col: str = "location_city"
) -> pd.DataFrame:
    """Create aggregated weather profile per location."""
    profile = (
        df.groupby(location_col)
        .agg(
            {
                "temperature_celsius": ["mean", "std", "min", "max"],
                "humidity_percent": ["mean", "std"],
                "wind_speed_kmh": ["mean", "std"],
                "condition": lambda x: x.value_counts().to_dict(),
            }
        )
        .reset_index()
    )

    profile.columns = [
        "location",
        "avg_temp",
        "std_temp",
        "min_temp",
        "max_temp",
        "avg_humidity",
        "std_humidity",
        "avg_wind",
        "std_wind",
        "condition_dist",
    ]

    return profile


def merge_weather_location_features(
    base_df: pd.DataFrame, weather_df: pd.DataFrame, location_col: str = "location_id"
) -> pd.DataFrame:
    """Merge weather-location features to base dataframe."""
    weather_features = create_weather_location_features(weather_df)

    result = pd.concat([base_df, weather_features], axis=1)

    return result


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        weather = pd.read_csv("data/raw/weather.csv")
        weather_loc_features = create_weather_location_features(weather)
        weather_loc_features.to_csv("data/features/weather_location.csv", index=False)
        print(f"Created weather-location features: {weather_loc_features.shape}")
        print(f"Columns: {list(weather_loc_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
