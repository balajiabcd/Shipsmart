import os
import logging
import requests
from datetime import datetime
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.base_url = os.getenv(
            "OPENWEATHERMAP_BASE_URL", "https://api.openweathermap.org/data/2.5"
        )
        if not self.api_key:
            logger.warning("OPENWEATHERMAP_API_KEY not set")

    def get_current_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Get current weather for a city."""
        url = f"{self.base_url}/weather"
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.error("Invalid API key for OpenWeatherMap")
            elif response.status_code == 404:
                logger.warning(f"City not found: {city}")
            else:
                logger.error(f"Weather API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None

    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict[str, Any]]:
        """Get weather forecast for a city."""
        url = f"{self.base_url}/forecast"
        params = {"q": city, "appid": self.api_key, "units": "metric", "cnt": days * 8}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Forecast API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None

    def get_weather_by_coords(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get weather by coordinates."""
        url = f"{self.base_url}/weather"
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None


def get_major_cities_weather(cities: List[str]) -> Dict[str, Optional[Dict]]:
    """Get current weather for multiple cities."""
    api = WeatherAPI()
    results = {}
    for city in cities:
        results[city] = api.get_current_weather(city)
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api = WeatherAPI()
    weather = api.get_current_weather("Berlin")
    print(weather)
