import pytest
import numpy as np
import joblib
from pathlib import Path


class TestMLModels:
    """Test ML model functions (Milestone 379)"""

    @pytest.fixture
    def sample_features(self):
        """Create sample feature array for testing"""
        return np.random.rand(1, 18)

    @pytest.fixture
    def sample_features_df(self):
        """Create sample DataFrame for testing"""
        import pandas as pd

        columns = [
            "distance_km",
            "weather_severity",
            "traffic_index",
            "time_of_day",
            "day_of_week",
            "driver_rating",
            "vehicle_type",
            "warehouse_load",
            "route_complexity",
            "demand_level",
            "is_rush_hour",
            "is_weekend",
            "is_holiday",
            "origin_lat",
            "origin_lng",
            "dest_lat",
            "dest_lng",
            "hour",
        ]
        return pd.DataFrame(np.random.rand(5, 18), columns=columns)

    @pytest.mark.skipif(
        not Path("models/best_classifier.pkl").exists(), reason="Model not found"
    )
    def test_model_loading(self):
        """Test model can be loaded"""
        model = joblib.load("models/best_classifier.pkl")
        assert model is not None

    @pytest.mark.skipif(
        not Path("models/best_classifier.pkl").exists(), reason="Model not found"
    )
    def test_prediction_output_type(self, sample_features):
        """Test prediction returns correct type"""
        model = joblib.load("models/best_classifier.pkl")
        prediction = model.predict(sample_features)
        assert isinstance(prediction, (np.ndarray, np.integer, int))

    @pytest.mark.skipif(
        not Path("models/best_classifier.pkl").exists(), reason="Model not found"
    )
    def test_prediction_consistency(self, sample_features):
        """Test predictions are consistent"""
        model = joblib.load("models/best_classifier.pkl")
        pred1 = model.predict(sample_features)[0]
        pred2 = model.predict(sample_features)[0]
        assert pred1 == pred2

    @pytest.mark.skipif(
        not Path("models/best_regressor.pkl").exists(), reason="Model not found"
    )
    def test_regressor_output(self):
        """Test regressor returns numeric value"""
        model = joblib.load("models/best_regressor.pkl")
        features = np.random.rand(1, 18)
        prediction = model.predict(features)
        assert isinstance(prediction[0], (np.floating, float))

    @pytest.mark.skipif(
        not Path("models/best_classifier.pkl").exists(), reason="Model not found"
    )
    def test_feature_count_validation(self, sample_features_df):
        """Test model accepts correct feature count"""
        model = joblib.load("models/best_classifier.pkl")
        # Should not raise
        prediction = model.predict(sample_features_df)
        assert len(prediction) == len(sample_features_df)
