import os
import logging
import requests
from typing import Optional, Dict, Any, Tuple, List

logger = logging.getLogger(__name__)


class TrafficAPI:
    def __init__(self):
        self.tomtom_key = os.getenv("TOMTOM_API_KEY")
        self.tomtom_base_url = os.getenv("TOMTOM_BASE_URL", "https://api.tomtom.com")

    def get_traffic_flow(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get traffic flow data for a location using TomTom Traffic Flow API."""
        if not self.tomtom_key or self.tomtom_key == "your_tomtom_api_key":
            logger.warning("TOMTOM_API_KEY not set or is placeholder")
            return None

        url = f"{self.tomtom_base_url}/traffic/services/4/flowSegmentData/absolute/10/{lat},{lon}"
        params = {"key": self.tomtom_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.error("Invalid TomTom API key")
            else:
                logger.error(f"TomTom API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None

    def get_route_traffic(
        self, origin: Tuple[float, float], destination: Tuple[float, float]
    ) -> Optional[Dict[str, Any]]:
        """Get route traffic information using TomTom Routing API."""
        if not self.tomtom_key or self.tomtom_key == "your_tomtom_api_key":
            logger.warning("TOMTOM_API_KEY not set or is placeholder")
            return None

        url = f"{self.tomtom_base_url}/routing/1/calculateRoute/{origin[0]},{origin[1]}:{destination[0]},{destination[1]}"
        params = {
            "key": self.tomtom_key,
            "traffic": "true",
            "travelTime": "best",
            "routeRepresentationForBestOrder": "travelTime",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.error("Invalid TomTom API key")
            else:
                logger.error(f"TomTom Routing API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None

    def get_traffic_incidents(
        self, bounding_box: Tuple[float, float, float, float]
    ) -> Optional[Dict[str, Any]]:
        """Get traffic incidents within a bounding box using TomTom Traffic Incidents API."""
        if not self.tomtom_key or self.tomtom_key == "your_tomtom_api_key":
            logger.warning("TOMTOM_API_KEY not set")
            return None

        url = f"{self.tomtom_base_url}/traffic/services/4/incident_details/s3"
        params = {
            "key": self.tomtom_key,
            "bbox": f"{bounding_box[0]},{bounding_box[1]},{bounding_box[2]},{bounding_box[3]}",
            "time": "published",
            "language": "en-US",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None

    def get_route_eta(
        self, waypoints: List[Tuple[float, float]]
    ) -> Optional[Dict[str, Any]]:
        """Get estimated time of arrival for multiple waypoints."""
        if not self.tomtom_key or self.tomtom_key == "your_tomtom_api_key":
            logger.warning("TOMTOM_API_KEY not set")
            return None

        waypoint_str = ":".join([f"{lat},{lon}" for lat, lon in waypoints])
        url = f"{self.tomtom_base_url}/routing/1/calculateRoute/{waypoint_str}"
        params = {"key": self.tomtom_key, "travelTime": "best", "routeType": "fastest"}

        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api = TrafficAPI()
    result = api.get_traffic_flow(52.52, 13.405)
    print(result)
