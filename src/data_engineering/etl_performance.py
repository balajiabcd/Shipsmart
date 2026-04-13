"""
ETL Pipeline for Performance Data (Drivers and Warehouse)
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_drivers_performance(file_path="data/raw/drivers_performance.csv"):
    """Extract drivers performance data from CSV."""
    print(f"Extracting drivers performance from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def extract_warehouse_performance(file_path="data/raw/warehouse_performance.csv"):
    """Extract warehouse performance data from CSV."""
    print(f"Extracting warehouse performance from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_drivers_performance(df):
    """Transform drivers performance data."""
    print("Transforming drivers performance data...")

    df["driver_id"] = df["driver_id"].str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["rating"] = df["rating"].clip(lower=0, upper=5)
    df["total_deliveries"] = df["total_deliveries"].fillna(0).astype(int)
    df["on_time_deliveries"] = df["on_time_deliveries"].fillna(0).astype(int)
    df["late_deliveries"] = df["late_deliveries"].fillna(0).astype(int)
    df["customer_complaints"] = df["customer_complaints"].fillna(0).astype(int)
    df["accidents"] = df["accidents"].fillna(0).astype(int)
    df["fuel_efficiency"] = df["fuel_efficiency"].fillna(df["fuel_efficiency"].median())
    df["overtime_hours"] = df["overtime_hours"].fillna(0)

    df["on_time_rate"] = df["on_time_deliveries"] / df["total_deliveries"].replace(0, 1)
    df["on_time_rate"] = df["on_time_rate"].clip(lower=0, upper=1)

    print(f"Transformed {len(df)} driver performance records")
    return df


def transform_warehouse_performance(df):
    """Transform warehouse performance data."""
    print("Transforming warehouse performance data...")

    df["warehouse_id"] = df["warehouse_id"].str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["inbound_volume"] = df["inbound_volume"].fillna(0).astype(int)
    df["outbound_volume"] = df["outbound_volume"].fillna(0).astype(int)
    df["throughput"] = df["throughput"].fillna(0).astype(int)
    df["delays_count"] = df["delays_count"].fillna(0).astype(int)
    df["staff_count"] = df["staff_count"].fillna(0).astype(int)
    df["returns_received"] = df["returns_received"].fillna(0).astype(int)

    df["avg_processing_time_minutes"] = df["avg_processing_time_minutes"].fillna(
        df["avg_processing_time_minutes"].median()
    )
    df["efficiency_score"] = df["efficiency_score"].fillna(
        df["efficiency_score"].median()
    )
    df["overtime_hours"] = df["overtime_hours"].fillna(0)
    df["error_rate"] = df["error_rate"].fillna(0)

    print(f"Transformed {len(df)} warehouse performance records")
    return df


def load_drivers_performance(df, connection_string):
    """Load drivers performance data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("drivers_performance", engine, if_exists="replace", index=False)
    print(f"Successfully loaded drivers_performance to database")


def load_warehouse_performance(df, connection_string):
    """Load warehouse performance data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("warehouse_performance", engine, if_exists="replace", index=False)
    print(f"Successfully loaded warehouse_performance to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df_drivers = extract_drivers_performance()
    df_drivers = transform_drivers_performance(df_drivers)
    load_drivers_performance(df_drivers, conn_string)

    df_warehouse = extract_warehouse_performance()
    df_warehouse = transform_warehouse_performance(df_warehouse)
    load_warehouse_performance(df_warehouse, conn_string)

    print("Performance ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
