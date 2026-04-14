import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

CITY_MAPPING = {
    "Berlin": "BER",
    "Munich": "MUN",
    "Hamburg": "HAM",
    "Frankfurt": "FRA",
    "Leipzig": "LEJ",
    "Cologne": "CGN",
    "Stuttgart": "STR",
    "Dusseldorf": "DUS",
    "Dortmund": "DTM",
    "Essen": "ESS",
}

REVERSE_CITY_MAPPING = {v: k for k, v in CITY_MAPPING.items()}


def merge_weather_data() -> pd.DataFrame:
    """Merge external weather API data with simulated data."""
    from src.external_apis.weather_api import WeatherAPI

    weather_sim = pd.read_csv("data/raw/weather.csv")
    weather_api = WeatherAPI()

    real_weather = []
    for location_id, city in REVERSE_CITY_MAPPING.items():
        data = weather_api.get_current_weather(city)
        if data and "main" in data:
            real_weather.append(
                {
                    "location_id": location_id,
                    "city": city,
                    "real_temperature": data["main"].get("temp"),
                    "real_humidity": data["main"].get("humidity"),
                    "real_condition": data["weather"][0].get("main")
                    if data.get("weather")
                    else None,
                    "real_wind_speed": data["wind"].get("speed")
                    if data.get("wind")
                    else None,
                    "timestamp": datetime.now().isoformat(),
                }
            )

    if not real_weather:
        logger.warning("No real weather data fetched, using simulated data only")
        return weather_sim

    real_df = pd.DataFrame(real_weather)

    merged = pd.merge(
        weather_sim, real_df, on="location_id", how="left", suffixes=("_sim", "_real")
    )

    return merged


def merge_traffic_data() -> pd.DataFrame:
    """Merge external traffic API data with simulated data."""
    from src.external_apis.traffic_api import TrafficAPI

    traffic_sim = pd.read_csv("data/raw/traffic.csv")
    traffic_api = TrafficAPI()

    real_traffic = []
    locations = (
        traffic_sim[["location_id", "latitude", "longitude"]].drop_duplicates().head(10)
    )

    for _, row in locations.iterrows():
        data = traffic_api.get_traffic_flow(row["latitude"], row["longitude"])
        if data and "flowSegmentData" in data:
            real_traffic.append(
                {
                    "location_id": row["location_id"],
                    "real_current_speed": data["flowSegmentData"].get("currentSpeed"),
                    "real_free_flow_speed": data["flowSegmentData"].get(
                        "freeFlowSpeed"
                    ),
                    "real_confidence": data["flowSegmentData"].get("confidence"),
                    "timestamp": datetime.now().isoformat(),
                }
            )

    if not real_traffic:
        logger.warning("No real traffic data fetched, using simulated data only")
        return traffic_sim

    real_df = pd.DataFrame(real_traffic)

    merged = pd.merge(
        traffic_sim, real_df, on="location_id", how="left", suffixes=("_sim", "_real")
    )

    return merged


def merge_holiday_data() -> pd.DataFrame:
    """Merge external holiday API data with simulated data."""
    from src.external_apis.holiday_api import HolidayAPI

    holidays_sim = pd.read_csv("data/raw/holidays.csv")
    holiday_api = HolidayAPI()

    current_year = datetime.now().year
    real_holidays = holiday_api.get_holidays(current_year, "DE")

    if not real_holidays:
        logger.warning("No real holiday data fetched, using simulated data only")
        return holidays_sim

    real_holiday_df = pd.DataFrame(
        [
            {
                "date": h["date"],
                "real_local_name": h.get("localName"),
                "real_name": h.get("name"),
                "real_fixed": h.get("fixed", False),
                "real_counties": h.get("counties", None),
            }
            for h in real_holidays
        ]
    )

    if "date" not in holidays_sim.columns:
        logger.warning("Simulated holidays has no date column")
        return holidays_sim

    merged = pd.merge(
        holidays_sim, real_holiday_df, on="date", how="left", suffixes=("_sim", "_real")
    )

    return merged


def merge_all_external_data() -> Dict[str, pd.DataFrame]:
    """Merge all external data sources with simulated data."""
    results = {}

    try:
        results["weather"] = merge_weather_data()
        logger.info(f"Merged weather data: {len(results['weather'])} records")
    except Exception as e:
        logger.error(f"Failed to merge weather data: {e}")

    try:
        results["traffic"] = merge_traffic_data()
        logger.info(f"Merged traffic data: {len(results['traffic'])} records")
    except Exception as e:
        logger.error(f"Failed to merge traffic data: {e}")

    try:
        results["holidays"] = merge_holiday_data()
        logger.info(f"Merged holidays data: {len(results['holidays'])} records")
    except Exception as e:
        logger.error(f"Failed to merge holidays data: {e}")

    return results


def save_merged_data(output_dir: str = "data/processed"):
    """Save all merged data to processed directory."""
    import os

    os.makedirs(output_dir, exist_ok=True)

    results = merge_all_external_data()

    for name, df in results.items():
        filepath = os.path.join(output_dir, f"{name}_enriched.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"Saved {name}_enriched.csv with {len(df)} records")

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    save_merged_data()
