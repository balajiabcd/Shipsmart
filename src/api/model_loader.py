import os
import logging
import joblib
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


class DelayPredictor:
    def __init__(self, model_name: str = "xgboost"):
        self.model_name = model_name
        self.model = None
        self.scaler = None
        self.feature_names = None
        self._load_model()

    def _load_model(self):
        model_path = os.path.join(MODEL_DIR, f"{self.model_name}_classifier.joblib")
        scaler_path = os.path.join(MODEL_DIR, f"{self.model_name}_scaler.joblib")

        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                logger.info(f"Loaded model: {model_path}")
            except Exception as e:
                logger.warning(f"Could not load model: {e}")
                self.model = None
        else:
            logger.warning(f"Model not found: {model_path}")
            self.model = None

        if os.path.exists(scaler_path):
            try:
                self.scaler = joblib.load(scaler_path)
            except Exception as e:
                logger.warning(f"Could not load scaler: {e}")

    def _prepare_features(self, request_data: dict) -> pd.DataFrame:
        features = {
            "origin_lat": request_data.get("origin_lat", 0),
            "origin_lon": request_data.get("origin_lon", 0),
            "destination_lat": request_data.get("destination_lat", 0),
            "destination_lon": request_data.get("destination_lon", 0),
            "scheduled_date": request_data.get("scheduled_date", ""),
            "scheduled_time": request_data.get("scheduled_time", ""),
        }

        if request_data.get("scheduled_date"):
            try:
                from datetime import datetime

                date = pd.to_datetime(request_data["scheduled_date"])
                features["day_of_week"] = date.dayofweek
                features["month"] = date.month
                features["is_weekend"] = 1 if date.dayofweek >= 5 else 0
            except:
                features["day_of_week"] = 0
                features["month"] = 1
                features["is_weekend"] = 0
        else:
            features["day_of_week"] = 0
            features["month"] = 1
            features["is_weekend"] = 0

        if request_data.get("scheduled_time"):
            try:
                hour = int(request_data["scheduled_time"].split(":")[0])
                features["hour_of_day"] = hour
                features["is_rush_hour"] = 1 if hour in [7, 8, 9, 17, 18, 19] else 0
            except:
                features["hour_of_day"] = 12
                features["is_rush_hour"] = 0
        else:
            features["hour_of_day"] = 12
            features["is_rush_hour"] = 0

        features["distance_km"] = self._calculate_distance(
            features["origin_lat"],
            features["origin_lon"],
            features["destination_lat"],
            features["destination_lon"],
        )

        features["weather_severity"] = 0.3
        features["traffic_index"] = 0.5
        features["driver_experience"] = 0.7
        features["warehouse_efficiency"] = 0.8

        df = pd.DataFrame([features])

        if self.feature_names:
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_names]

        return df

    def _calculate_distance(self, lat1, lon1, lat2, lon2) -> float:
        import math

        if lat1 == 0 and lon1 == 0:
            return 50.0
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(min(1, a)))
        return R * c

    def predict(self, request_data: dict) -> Dict[str, Any]:
        if self.model is None:
            return self._mock_prediction(request_data)

        try:
            features = self._prepare_features(request_data)

            if self.scaler is not None:
                features = self.scaler.transform(features)

            proba = self.model.predict_proba(features)[0]
            delay_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

            return {
                "predicted_delay": delay_prob > 0.5,
                "delay_probability": delay_prob,
                "confidence": "high"
                if delay_prob > 0.8 or delay_prob < 0.2
                else "medium",
                "model_version": f"{self.model_name}_v1.0",
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._mock_prediction(request_data)

    def _mock_prediction(self, request_data: dict) -> Dict[str, Any]:
        distance = self._calculate_distance(
            request_data.get("origin_lat", 0),
            request_data.get("origin_lon", 0),
            request_data.get("destination_lat", 0),
            request_data.get("destination_lon", 0),
        )

        base_prob = 0.3
        if distance > 100:
            base_prob += 0.2
        elif distance > 50:
            base_prob += 0.1

        hour = 12
        if request_data.get("scheduled_time"):
            try:
                hour = int(request_data["scheduled_time"].split(":")[0])
            except:
                pass
        if hour in [8, 9, 17, 18, 19]:
            base_prob += 0.15

        delay_prob = min(0.95, base_prob)

        return {
            "predicted_delay": delay_prob > 0.5,
            "delay_probability": delay_prob,
            "confidence": "high" if delay_prob > 0.8 or delay_prob < 0.2 else "medium",
            "model_version": f"{self.model_name}_v1.0",
        }


_predictor = None


def get_predictor() -> DelayPredictor:
    global _predictor
    if _predictor is None:
        _predictor = DelayPredictor()
    return _predictor
