"""
ETL Pipeline for Drivers Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_drivers(file_path="data/raw/drivers.csv"):
    """Extract drivers data from CSV."""
    print(f"Extracting drivers from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_drivers(df):
    """Transform drivers data."""
    print("Transforming drivers data...")

    df["full_name"] = df["full_name"].str.strip()
    df["license_number"] = df["license_number"].str.strip()
    df["status"] = df["status"].str.lower().str.strip()

    df["license_expiry"] = pd.to_datetime(df["license_expiry"], errors="coerce")
    df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")

    df["rating"] = df["rating"].clip(lower=0, upper=5)
    df["on_time_rate"] = df["on_time_rate"].clip(lower=0, upper=1)
    df["total_deliveries"] = df["total_deliveries"].fillna(0).astype(int)

    df["contact_phone"] = (
        df["contact_phone"].astype(str).str.replace(r"^\+49", "0", regex=True)
    )

    df["license_status"] = df["license_expiry"].apply(
        lambda x: "expired" if pd.notna(x) and x < pd.Timestamp.now() else "valid"
    )

    df["experience_years"] = (pd.Timestamp.now() - df["hire_date"]).dt.days / 365.25
    df["experience_years"] = df["experience_years"].clip(lower=0)

    df["performance_score"] = (df["rating"] * 0.6 + df["on_time_rate"] * 0.4) * 100

    print(f"Transformed {len(df)} records")
    return df


def load_drivers(df, connection_string):
    """Load drivers data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("drivers", engine, if_exists="replace", index=False)
    print(f"Successfully loaded drivers to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_drivers()
    df = transform_drivers(df)
    load_drivers(df, conn_string)

    print("Drivers ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
