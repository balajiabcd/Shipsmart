"""
ETL Pipeline for Delivery Events Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_delivery_events(file_path="data/raw/delivery_events.csv"):
    """Extract delivery events data from CSV."""
    print(f"Extracting delivery events from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_delivery_events(df):
    """Transform delivery events data."""
    print("Transforming delivery events data...")

    df["order_id"] = df["order_id"].str.strip()
    df["location_id"] = df["location_id"].str.strip()
    df["event_type"] = df["event_type"].str.lower().str.strip()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df["driver_id"] = df["driver_id"].fillna("UNKNOWN")
    df["notes"] = df["notes"].fillna("")

    df = df.dropna(subset=["event_id", "order_id", "timestamp"])

    event_order = {
        "created": 1,
        "picked_up": 2,
        "out_for_delivery": 3,
        "failed_attempt": 4,
        "delivered": 5,
    }
    df["event_sequence"] = df["event_type"].map(event_order).fillna(0)

    print(f"Transformed {len(df)} records")
    return df


def load_delivery_events(df, connection_string):
    """Load delivery events data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("delivery_events", engine, if_exists="replace", index=False)
    print(f"Successfully loaded delivery_events to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_delivery_events()
    df = transform_delivery_events(df)
    load_delivery_events(df, conn_string)

    print("Delivery Events ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
