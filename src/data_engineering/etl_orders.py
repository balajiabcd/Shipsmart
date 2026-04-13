"""
ETL Pipeline for Orders Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_orders(file_path="data/raw/orders.csv"):
    """Extract orders data from CSV."""
    print(f"Extracting orders from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_orders(df):
    """Transform orders data."""
    print("Transforming orders data...")

    # Handle missing values
    df["driver_id"] = df["driver_id"].fillna("UNKNOWN")
    df["warehouse_id"] = df["warehouse_id"].fillna("UNKNOWN")
    df["package_weight_kg"] = df["package_weight_kg"].fillna(
        df["package_weight_kg"].median()
    )

    # Clean dates
    df["order_time"] = pd.to_datetime(df["order_time"], errors="coerce")
    df["scheduled_delivery_time"] = pd.to_datetime(
        df["scheduled_delivery_time"], errors="coerce"
    )
    df["actual_delivery_time"] = pd.to_datetime(
        df["actual_delivery_time"], errors="coerce"
    )

    # Remove records with invalid order times
    df = df[df["order_time"].notna()]

    # Standardize status values
    df["status"] = df["status"].str.lower().str.strip()

    # Calculate delay if not present
    df["delay_minutes"] = df.apply(
        lambda row: (
            int(
                (
                    row["actual_delivery_time"] - row["scheduled_delivery_time"]
                ).total_seconds()
                / 60
            )
            if pd.notna(row["actual_delivery_time"])
            and pd.notna(row["scheduled_delivery_time"])
            else None
        ),
        axis=1,
    )
    df["delay_minutes"] = df["delay_minutes"].clip(lower=0)

    print(f"Transformed {len(df)} records")
    return df


def load_orders(df, connection_string):
    """Load orders data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("orders", engine, if_exists="replace", index=False)
    print(f"Successfully loaded orders to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    # Connection string
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    # Extract
    df = extract_orders()

    # Transform
    df = transform_orders(df)

    # Load
    load_orders(df, conn_string)

    print("ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
