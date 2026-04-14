import pandas as pd
import numpy as np
from typing import Dict, Optional


CONDITION_SEVERITY_MAP = {
    "clear": 0,
    "sunny": 0,
    "partly_cloudy": 1,
    "cloudy": 1,
    "overcast": 1,
    "fog": 2,
    "mist": 2,
    "rain": 3,
    "drizzle": 3,
    "light_rain": 2,
    "heavy_rain": 4,
    "snow": 4,
    "light_snow": 3,
    "heavy_snow": 5,
    "sleet": 4,
    "storm": 5,
    "thunderstorm": 5,
    "wind": 2,
}


def calculate_temperature_severity(temp: float) -> int:
    """Calculate severity based on temperature."""
    if pd.isna(temp):
        return 1
    if temp < -10 or temp > 40:
        return 4
    if temp < 0 or temp > 35:
        return 3
    if temp < 5 or temp > 30:
        return 2
    return 1


def calculate_wind_severity(wind_speed: float) -> int:
    """Calculate severity based on wind speed (km/h)."""
    if pd.isna(wind_speed):
        return 0
    if wind_speed > 60:
        return 4
    if wind_speed > 40:
        return 3
    if wind_speed > 20:
        return 2
    if wind_speed > 10:
        return 1
    return 0


def calculate_humidity_severity(humidity: float) -> int:
    """Calculate severity based on humidity."""
    if pd.isna(humidity):
        return 0
    if humidity > 90 or humidity < 20:
        return 3
    if humidity > 80 or humidity < 30:
        return 2
    return 0


def calculate_visibility_severity(visibility: float) -> int:
    """Calculate severity based on visibility (km)."""
    if pd.isna(visibility):
        return 0
    if visibility < 0.5:
        return 4
    if visibility < 2:
        return 3
    if visibility < 5:
        return 2
    if visibility < 10:
        return 1
    return 0


def create_weather_severity(
    df: pd.DataFrame,
    temp_col: str = "temperature_celsius",
    condition_col: str = "condition",
    wind_col: str = "wind_speed_kmh",
    humidity_col: str = "humidity_percent",
    visibility_col: str = "visibility_km",
) -> pd.DataFrame:
    """Create weather severity index from weather data.

    Args:
        df: Input dataframe with weather columns
        temp_col: Temperature column name
        condition_col: Weather condition column name
        wind_col: Wind speed column name
        humidity_col: Humidity column name
        visibility_col: Visibility column name

    Returns:
        DataFrame with weather severity features
    """
    features = pd.DataFrame(index=df.index)

    features["temp_severity"] = df[temp_col].apply(calculate_temperature_severity)

    features["condition_severity"] = (
        df[condition_col].map(CONDITION_SEVERITY_MAP).fillna(1)
    )

    features["wind_severity"] = df[wind_col].apply(calculate_wind_severity)

    features["humidity_severity"] = df[humidity_col].apply(calculate_humidity_severity)

    features["visibility_severity"] = df[visibility_col].apply(
        calculate_visibility_severity
    )

    features["weather_severity_index"] = (
        features["temp_severity"]
        + features["condition_severity"]
        + features["wind_severity"]
        + features["humidity_severity"]
        + features["visibility_severity"]
    )

    features["weather_severity_level"] = pd.cut(
        features["weather_severity_index"],
        bins=[-1, 3, 6, 9, 25],
        labels=["low", "medium", "high", "extreme"],
    ).astype(str)

    features["is_bad_weather"] = (features["weather_severity_index"] >= 6).astype(int)
    features["is_severe_weather"] = (features["weather_severity_index"] >= 10).astype(
        int
    )

    return features


def create_weather_category(
    df: pd.DataFrame, condition_col: str = "condition"
) -> pd.Series:
    """Create simplified weather category."""
    condition = df[condition_col].str.lower().fillna("clear")

    categories = []
    for c in condition:
        if c in ["clear", "sunny"]:
            categories.append("clear")
        elif c in ["partly_cloudy", "cloudy", "overcast"]:
            categories.append("cloudy")
        elif c in ["fog", "mist"]:
            categories.append("fog")
        elif c in ["rain", "drizzle", "light_rain", "heavy_rain"]:
            categories.append("rain")
        elif c in ["snow", "light_snow", "heavy_snow", "sleet"]:
            categories.append("snow")
        elif c in ["storm", "thunderstorm"]:
            categories.append("storm")
        else:
            categories.append("other")

    return pd.Series(categories, index=df.index)


if __name__ == "__main__":
    import os

    os.makedirs("data/features", exist_ok=True)

    try:
        weather = pd.read_csv("data/raw/weather.csv")
        weather_features = create_weather_severity(weather)
        weather_features.to_csv("data/features/weather_features.csv", index=False)
        print(f"Created weather features: {weather_features.shape}")
        print(f"Columns: {list(weather_features.columns)}")
    except Exception as e:
        print(f"Error: {e}")
