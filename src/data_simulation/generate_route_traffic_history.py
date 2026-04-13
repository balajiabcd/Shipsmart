import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(55)
random.seed(55)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 100000

route_ids = [f"RTE-{str(i).zfill(4)}" for i in range(1, 1001)]
traffic_levels = [
    "low",
    "medium",
    "high",
    "severe",
    "light",
    "moderate",
    "heavy",
    "blocked",
]

traffic_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_records):
    route = random.choice(route_ids)
    date = base_date + timedelta(days=random.randint(0, 730))
    hour = random.randint(0, 23)
    traffic_level = random.choice(traffic_levels)
    avg_speed = random.uniform(30, 160)

    traffic_data.append(
        {
            "route_id": route,
            "date": date.strftime("%Y-%m-%d"),
            "hour": hour,
            "traffic_level": traffic_level,
            "avg_speed_kmh": round(avg_speed, 1),
            "travel_time_multiplier": round(random.uniform(1.0, 4.0), 2),
            "incidents_count": random.randint(0, 5),
        }
    )

df = pd.DataFrame(traffic_data)

missing_speed = np.random.choice(n_records, size=int(0.02 * n_records), replace=False)
df.loc[missing_speed, "avg_speed_kmh"] = None

inconsistent_level = np.random.choice(
    n_records, size=int(0.02 * n_records), replace=False
)
df.loc[inconsistent_level, "traffic_level"] = "unknown"

output_path = os.path.join(output_dir, "route_traffic_history.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} route traffic history records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing avg_speed: {len(missing_speed)} ({100 * len(missing_speed) / n_records:.2f}%)"
)
print(
    f"- Inconsistent traffic_level: {len(inconsistent_level)} ({100 * len(inconsistent_level) / n_records:.2f}%)"
)
print(f"\nTraffic level distribution:")
print(df["traffic_level"].value_counts())
