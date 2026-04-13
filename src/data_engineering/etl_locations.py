"""
ETL Pipeline for Locations Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


LOCATION_COORDS = {
    "Munich": (48.1351, 11.582),
    "Berlin": (52.52, 13.405),
    "Hamburg": (53.5511, 9.9937),
    "Frankfurt": (50.1109, 8.6821),
    "Cologne": (50.9375, 6.9603),
    "Stuttgart": (48.7758, 9.1829),
    "Munich": (48.1351, 11.582),
}


def extract_locations(file_path="data/raw/locations.csv"):
    """Extract locations data from CSV."""
    print(f"Extracting locations from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def transform_locations(df):
    """Transform locations data."""
    print("Transforming locations data...")

    df["city"] = df["city"].str.strip()
    df["region"] = df["region"].str.strip()
    df["location_type"] = df["location_type"].str.lower().str.strip()

    for idx, row in df.iterrows():
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            city = row["city"]
            if city in LOCATION_COORDS:
                df.at[idx, "latitude"] = LOCATION_COORDS[city][0]
                df.at[idx, "longitude"] = LOCATION_COORDS[city][1]

    median_lat = df["latitude"].median()
    median_lon = df["longitude"].median()
    df["latitude"] = df["latitude"].fillna(median_lat)
    df["longitude"] = df["longitude"].fillna(median_lon)

    df["population"] = df["population"].fillna(df["population"].median())

    df["postal_code"] = df["postal_code"].fillna(0).astype(int)

    print(f"Transformed {len(df)} records")
    return df


def load_locations(df, connection_string):
    """Load locations data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("locations", engine, if_exists="replace", index=False)
    print(f"Successfully loaded locations to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_locations()
    df = transform_locations(df)
    load_locations(df, conn_string)

    print("Locations ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
