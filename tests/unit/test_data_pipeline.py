import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_engineering.etl.orders import transform_orders
from data_engineering.etl.drivers import transform_drivers
from data_engineering.etl.weather import transform_weather


class TestDataPipeline:
    """Test data pipeline ETL functions (Milestone 377)"""

    @pytest.fixture
    def sample_orders_df(self):
        return pd.DataFrame(
            {
                "order_id": ["ORD001", "ORD002", "ORD003"],
                "origin": ["Berlin", "Munich", "Hamburg"],
                "destination": ["Munich", "Berlin", "Stuttgart"],
                "distance_km": [100, 150, 80],
                "order_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "expected_delivery_date": ["2024-01-02", "2024-01-04", "2024-01-04"],
                "status": ["delivered", "delivered", "in_transit"],
            }
        )

    @pytest.fixture
    def sample_drivers_df(self):
        return pd.DataFrame(
            {
                "driver_id": ["DRV001", "DRV002"],
                "name": ["John Doe", "Jane Smith"],
                "rating": [4.5, 4.8],
                "experience_years": [5, 3],
                "status": ["active", "active"],
            }
        )

    def test_transform_orders(self, sample_orders_df):
        """Test order transformation"""
        result = transform_orders(sample_orders_df)
        assert "order_id" in result.columns
        assert "distance_km" in result.columns
        assert pd.api.types.is_numeric_dtype(result["distance_km"])

    def test_transform_drivers(self, sample_drivers_df):
        """Test driver transformation"""
        result = transform_drivers(sample_drivers_df)
        assert "driver_id" in result.columns
        assert "rating" in result.columns

    def test_handle_missing_values(self, sample_orders_df):
        """Test missing value handling"""
        df = sample_orders_df.copy()
        df.loc[0, "distance_km"] = np.nan
        result = transform_orders(df)
        assert result["distance_km"].isna().sum() == 0

    def test_validate_schema(self, sample_orders_df):
        """Test schema validation"""
        result = transform_orders(sample_orders_df)
        assert len(result) > 0
        assert result["order_id"].nunique() > 0
