import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from features.temporal_features import create_temporal_features
from features.distance_features import calculate_distance_features
from features.weather_features import create_weather_features
from features.driver_features import create_driver_features


class TestFeatureEngineering:
    """Test feature engineering functions (Milestone 378)"""

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame(
            {
                "order_date": pd.date_range("2024-01-01", periods=10, freq="D"),
                "distance_km": [50, 100, 75, 80, 60, 90, 120, 70, 85, 95],
                "weather_condition": [
                    "clear",
                    "rain",
                    "storm",
                    "clear",
                    "fog",
                    "snow",
                    "clear",
                    "rain",
                    "clear",
                    "storm",
                ],
                "driver_rating": [4.5, 4.8, 4.2, 4.9, 4.6, 4.3, 4.7, 4.4, 4.8, 4.5],
                "origin_lat": [52.52] * 10,
                "origin_lng": [13.405] * 10,
                "dest_lat": [
                    48.85,
                    52.52,
                    48.78,
                    52.52,
                    51.51,
                    49.79,
                    52.52,
                    52.52,
                    52.52,
                    52.52,
                ],
                "dest_lng": [
                    13.405,
                    13.405,
                    9.18,
                    13.405,
                    6.95,
                    9.99,
                    13.405,
                    13.405,
                    13.405,
                    13.405,
                ],
            }
        )

    def test_temporal_features(self, sample_df):
        """Test temporal feature creation"""
        result = create_temporal_features(sample_df)
        assert "hour" in result.columns
        assert "day_of_week" in result.columns
        assert "month" in result.columns
        assert "is_weekend" in result.columns

    def test_distance_features(self, sample_df):
        """Test distance feature calculation"""
        result = calculate_distance_features(sample_df)
        assert "distance_km" in result.columns
        assert "is_long_distance" in result.columns

    def test_weather_features(self, sample_df):
        """Test weather feature creation"""
        result = create_weather_features(sample_df)
        assert "weather_severity" in result.columns
        assert "is_bad_weather" in result.columns

    def test_driver_features(self, sample_df):
        """Test driver feature engineering"""
        result = create_driver_features(sample_df)
        assert "driver_rating" in result.columns
        assert "is_experienced" in result.columns

    def test_feature_range(self, sample_df):
        """Test feature value ranges"""
        result = create_temporal_features(sample_df)
        assert result["hour"].min() >= 0
        assert result["hour"].max() <= 23
        assert result["day_of_week"].min() >= 0
        assert result["day_of_week"].max() <= 6
