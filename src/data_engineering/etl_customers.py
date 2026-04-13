"""
ETL Pipeline for Customers Data
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import hashlib
import os


def extract_customers(file_path="data/raw/customers.csv"):
    """Extract customers data from CSV."""
    print(f"Extracting customers from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df


def anonymize_email(email):
    """Anonymize email address."""
    if pd.isna(email):
        return "unknown@example.com"
    local = email.split("@")[0]
    hash_val = hashlib.md5(local.encode()).hexdigest()[:8]
    return f"user_{hash_val}@example.com"


def anonymize_phone(phone):
    """Anonymize phone number."""
    if pd.isna(phone):
        return "0000000000"
    digits = "".join(filter(str.isdigit, str(phone)))
    return digits[-4:].rjust(10, "0")


def transform_customers(df):
    """Transform customers data."""
    print("Transforming customers data...")

    df["first_name"] = df["first_name"].str.strip()
    df["last_name"] = df["last_name"].str.strip()
    df["city"] = df["city"].str.strip()
    df["customer_type"] = df["customer_type"].str.lower().str.strip()
    df["preferred_shipping"] = df["preferred_shipping"].str.lower().str.strip()
    df["account_status"] = df["account_status"].str.lower().str.strip()

    df["email"] = df["email"].apply(anonymize_email)
    df["phone"] = df["phone"].apply(anonymize_phone)

    df["customer_since"] = pd.to_datetime(df["customer_since"], errors="coerce")

    df["credit_limit"] = df["credit_limit"].fillna(df["credit_limit"].median())

    df["postal_code"] = df["postal_code"].fillna(0).astype(int)

    df = df.drop_duplicates(subset=["customer_id"], keep="first")

    print(f"Transformed {len(df)} records")
    return df


def load_customers(df, connection_string):
    """Load customers data to database."""
    print(f"Loading {len(df)} records to database...")
    engine = create_engine(connection_string)
    df.to_sql("customers", engine, if_exists="replace", index=False)
    print(f"Successfully loaded customers to database")


def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )

    df = extract_customers()
    df = transform_customers(df)
    load_customers(df, conn_string)

    print("Customers ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_etl_pipeline()
