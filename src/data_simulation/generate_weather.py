import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(48)
random.seed(48)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_weather = 50000

cities = [
    "Berlin",
    "Munich",
    "Hamburg",
    "Frankfurt",
    "Stuttgart",
    "Cologne",
    "Dusseldorf",
    "Dortmund",
    "Leipzig",
    "Dresden",
]

conditions = ["clear", "cloudy", "rain", "snow", "fog", "storm"]
wind_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

weather_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_weather):
    city = random.choice(cities)
    date = base_date + timedelta(
        days=random.randint(0, 730), hours=random.randint(0, 23)
    )

    temp = random.uniform(-15, 35)
    humidity = random.uniform(20, 100)
    wind_speed = random.uniform(0, 80)

    weather_data.append(
        {
            "timestamp": date.strftime("%Y-%m-%d %H:%M"),
            "location_city": city,
            "temperature_celsius": round(temp, 1),
            "humidity_percent": round(humidity, 1),
            "wind_speed_kmh": round(wind_speed, 1),
            "wind_direction": random.choice(wind_directions),
            "condition": random.choice(conditions),
            "visibility_km": round(random.uniform(0.5, 50), 1),
        }
    )

df = pd.DataFrame(weather_data)

missing_temp = np.random.choice(n_weather, size=int(0.10 * n_weather), replace=False)
df.loc[missing_temp, "temperature_celsius"] = None

missing_humidity = np.random.choice(
    n_weather, size=int(0.08 * n_weather), replace=False
)
df.loc[missing_humidity, "humidity_percent"] = None

missing_wind = np.random.choice(n_weather, size=int(0.05 * n_weather), replace=False)
df.loc[missing_wind, "wind_speed_kmh"] = None

output_path = os.path.join(output_dir, "weather.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_weather} weather records with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing temperature: {len(missing_temp)} ({100 * len(missing_temp) / n_weather:.2f}%)"
)
print(
    f"- Missing humidity: {len(missing_humidity)} ({100 * len(missing_humidity) / n_weather:.2f}%)"
)
print(
    f"- Missing wind_speed: {len(missing_wind)} ({100 * len(missing_wind) / n_weather:.2f}%)"
)
print(f"\nCondition distribution:")
print(df["condition"].value_counts())
