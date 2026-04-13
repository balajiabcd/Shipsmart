"""
ETL Pipeline for Routes Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def extract_routes(file_path="data/raw/routes.csv"):
    """Extract routes data from CSV."""
    print(f"Extracting routes from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_routes(df):
    """Transform routes data."""
    print("Transforming routes data...")

    df["origin_city"] = df["origin_city"].str.strip()
    df["destination_city"] = df["destination_city"].str.strip()
    df["route_type"] = df["route_type"].str.lower().str.strip()
    df["traffic_level"] = df["traffic_level"].str.lower().str.strip()
    df["preferred_times"] = df["preferred_times"].str.lower().str.strip()

    df["distance_km"] = df["distance_km"].fillna(df["distance_km"].median())

    df["avg_duration_minutes"] = df["avg_duration_minutes"].fillna(
        (df["distance_km"] / 60).round() * 60
    )

    df = df.drop_duplicates(subset=["route_id"], keep="first")

    df["toll_roads"] = df["toll_roads"].map({True: "yes", False: "no"})

    print(f"Transformed {len(df)} records")
    return df


def load_routes(df, connection_string):
    """Load routes data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("routes", engine, if_exists="replace", index=False)
    print(f"Successfully loaded routes to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_routes()
    df = transform_routes(df)
    load_routes(df, conn_string)

    print("Routes ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
