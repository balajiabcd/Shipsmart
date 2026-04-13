"""
ETL Pipeline for Vehicles Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_vehicles(file_path="data/raw/vehicles.csv"):
    """Extract vehicles data from CSV."""
    print(f"Extracting vehicles from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_vehicles(df):
    """Transform vehicles data."""
    print("Transforming vehicles data...")

    df["vehicle_type"] = df["vehicle_type"].str.lower().str.strip()
    df["make"] = df["make"].str.strip()
    df["model"] = df["model"].str.strip()
    df["status"] = df["status"].str.lower().str.strip()
    df["fuel_type"] = df["fuel_type"].str.lower().str.strip()

    df["insurance_expiry"] = pd.to_datetime(df["insurance_expiry"], errors="coerce")
    df["maintenance_due"] = pd.to_datetime(df["maintenance_due"], errors="coerce")

    current_year = pd.Timestamp.now().year
    df["vehicle_age"] = current_year - df["manufacturing_year"]
    df["vehicle_age"] = df["vehicle_age"].clip(lower=0)

    df["capacity_kg"] = df["capacity_kg"].fillna(df["capacity_kg"].median())

    df["mileage"] = df["mileage"].fillna(0)

    df["insurance_status"] = df["insurance_expiry"].apply(
        lambda x: "expired" if pd.notna(x) and x < pd.Timestamp.now() else "valid"
    )

    df["maintenance_status"] = df["maintenance_due"].apply(
        lambda x: (
            "overdue"
            if pd.notna(x) and x < pd.Timestamp.now()
            else "upcoming"
            if pd.notna(x) and (x - pd.Timestamp.now()).days <= 30
            else "ok"
        )
    )

    vehicle_type_order = {"scooter": 1, "motorcycle": 2, "van": 3, "truck": 4}
    df["capacity_category"] = df["vehicle_type"].map(vehicle_type_order).fillna(5)

    print(f"Transformed {len(df)} records")
    return df


def load_vehicles(df, connection_string):
    """Load vehicles data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("vehicles", engine, if_exists="replace", index=False)
    print(f"Successfully loaded vehicles to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_vehicles()
    df = transform_vehicles(df)
    load_vehicles(df, conn_string)

    print("Vehicles ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
