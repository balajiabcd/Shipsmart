"""
ETL Pipeline for Weather Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_weather(file_path="data/raw/weather.csv"):
    """Extract weather data from CSV."""
    print(f"Extracting weather from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_weather(df):
    """Transform weather data."""
    print("Transforming weather data...")

    df["location_city"] = df["location_city"].str.strip()
    df["condition"] = df["condition"].str.lower().str.strip()
    df["wind_direction"] = df["wind_direction"].str.upper().str.strip()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    median_temp = df["temperature_celsius"].median()
    df["temperature_celsius"] = df["temperature_celsius"].fillna(median_temp)

    median_humidity = df["humidity_percent"].median()
    df["humidity_percent"] = df["humidity_percent"].fillna(median_humidity)

    median_wind = df["wind_speed_kmh"].median()
    df["wind_speed_kmh"] = df["wind_speed_kmh"].fillna(median_wind)

    df["visibility_km"] = df["visibility_km"].fillna(df["visibility_km"].median())

    df = df.dropna(subset=["timestamp", "location_city"])

    print(f"Transformed {len(df)} records")
    return df


def load_weather(df, connection_string):
    """Load weather data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("weather", engine, if_exists="replace", index=False)
    print(f"Successfully loaded weather to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_weather()
    df = transform_weather(df)
    load_weather(df, conn_string)

    print("Weather ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
