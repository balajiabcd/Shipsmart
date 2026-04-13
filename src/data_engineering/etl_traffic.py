"""
ETL Pipeline for Traffic Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_traffic(file_path="data/raw/traffic.csv"):
    """Extract traffic data from CSV."""
    print(f"Extracting traffic from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_traffic(df):
    """Transform traffic data."""
    print("Transforming traffic data...")

    df["route_id"] = df["route_id"].str.strip()
    df["congestion_level"] = df["congestion_level"].str.lower().str.strip()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df["avg_speed_kmh"] = df["avg_speed_kmh"].fillna(df["avg_speed_kmh"].median())
    df["traffic_volume"] = df["traffic_volume"].fillna(df["traffic_volume"].median())
    df["delay_minutes"] = df["delay_minutes"].fillna(0)

    congestion_order = {
        "low": 1,
        "medium": 2,
        "moderate": 2,
        "high": 3,
        "heavy": 4,
        "blocked": 5,
    }
    df["congestion_score"] = df["congestion_level"].map(congestion_order).fillna(2)

    print(f"Transformed {len(df)} records")
    return df


def load_traffic(df, connection_string):
    """Load traffic data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("traffic", engine, if_exists="replace", index=False)
    print(f"Successfully loaded traffic to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_traffic()
    df = transform_traffic(df)
    load_traffic(df, conn_string)

    print("Traffic ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
