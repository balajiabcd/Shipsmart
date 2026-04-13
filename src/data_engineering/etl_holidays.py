"""
ETL Pipeline for Holidays Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_holidays(file_path="data/raw/holidays.csv"):
    """Extract holidays data from CSV."""
    print(f"Extracting holidays from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_holidays(df):
    """Transform holidays data."""
    print("Transforming holidays data...")

    df["country"] = df["country"].str.strip()
    df["region"] = df["region"].str.strip()
    df["holiday_name"] = df["holiday_name"].str.strip()
    df["holiday_type"] = df["holiday_type"].str.lower().str.strip()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["celebrations_expected"] = df["celebrations_expected"].fillna(0).astype(int)

    df = df.dropna(subset=["date", "holiday_name"])

    print(f"Transformed {len(df)} records")
    return df


def load_holidays(df, connection_string):
    """Load holidays data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("holidays", engine, if_exists="replace", index=False)
    print(f"Successfully loaded holidays to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_holidays()
    df = transform_holidays(df)
    load_holidays(df, conn_string)

    print("Holidays ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
