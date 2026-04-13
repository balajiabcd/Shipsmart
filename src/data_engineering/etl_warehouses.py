"""
ETL Pipeline for Warehouses Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_warehouses(file_path="data/raw/warehouses.csv"):
    """Extract warehouses data from CSV."""
    print(f"Extracting warehouses from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_warehouses(df):
    """Transform warehouses data."""
    print("Transforming warehouses data...")

    df["warehouse_name"] = df["warehouse_name"].str.strip()
    df["city"] = df["city"].str.strip()
    df["manager_name"] = df["manager_name"].fillna("Unknown")
    df["manager_contact"] = df["manager_contact"].fillna("Unknown")
    df["email"] = df["email"].fillna("unknown@shipsmart.de")
    df["status"] = df["status"].str.lower().str.strip()
    df["zone"] = df["zone"].str.upper().str.strip()
    df["region"] = df["region"].str.strip()

    df["established_date"] = pd.to_datetime(df["established_date"], errors="coerce")

    df["capacity_sqm"] = df["capacity_sqm"].fillna(df["capacity_sqm"].median())

    df["operating_hours"] = df["operating_hours"].str.strip()

    print(f"Transformed {len(df)} records")
    return df


def load_warehouses(df, connection_string):
    """Load warehouses data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("warehouses", engine, if_exists="replace", index=False)
    print(f"Successfully loaded warehouses to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_warehouses()
    df = transform_warehouses(df)
    load_warehouses(df, conn_string)

    print("Warehouses ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
