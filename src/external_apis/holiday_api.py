import os
import logging
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


class HolidayAPI:
    BASE_URL = os.getenv("NAGER_DATE_BASE_URL", "https://date.nager.at/api/v3")

    def get_holidays(self, year: int, country: str = "DE") -> List[Dict[str, Any]]:
        """Get public holidays for a specific year and country."""
        url = f"{self.BASE_URL}/PublicHolidays/{year}/{country}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"No holidays found for {country} in {year}")
                return []
            else:
                logger.error(f"Holiday API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return []

    def get_next_holidays(
        self, country: str = "DE", days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get upcoming holidays within specified days."""
        url = f"{self.BASE_URL}/NextPublicHolidays/{country}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                holidays = response.json()
                cutoff = datetime.now() + timedelta(days=days)
                upcoming = []
                for holiday in holidays:
                    date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                    if date <= cutoff:
                        upcoming.append(holiday)
                return upcoming
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return []

    def is_holiday(self, date: str, country: str = "DE") -> bool:
        """Check if a specific date is a public holiday."""
        url = f"{self.BASE_URL}/IsTodayPublicHoliday/{country}"
        try:
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        return False

    def get_holidays_for_date_range(
        self, start_date: datetime, end_date: datetime, country: str = "DE"
    ) -> List[Dict[str, Any]]:
        """Get holidays within a date range."""
        all_holidays = []
        for year in range(start_date.year, end_date.year + 1):
            holidays = self.get_holidays(year, country)
            for holiday in holidays:
                holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                if start_date <= holiday_date <= end_date:
                    all_holidays.append(holiday)
        return all_holidays


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api = HolidayAPI()
    holidays = api.get_holidays(2026, "DE")
    print(f"Found {len(holidays)} holidays in 2026")
    for h in holidays[:5]:
        print(f"  {h['date']}: {h['name']}")
