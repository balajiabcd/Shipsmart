import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(49)
random.seed(49)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_traffic = 50000

route_ids = [f"RTE-{str(i).zfill(4)}" for i in range(1, 1001)]

congestion_levels = [
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

for i in range(n_traffic):
    date = base_date + timedelta(
        days=random.randint(0, 730), hours=random.randint(0, 23)
    )
    route = random.choice(route_ids)

    congestion = random.choice(congestion_levels)
    speed = random.uniform(20, 180)

    traffic_data.append(
        {
            "timestamp": date.strftime("%Y-%m-%d %H:%M"),
            "route_id": route,
            "hour": date.hour,
            "congestion_level": congestion,
            "avg_speed_kmh": round(speed, 1),
            "traffic_volume": random.randint(100, 8000),
            "delay_minutes": random.randint(0, 60)
            if congestion in ["high", "severe", "heavy"]
            else 0,
        }
    )

df = pd.DataFrame(traffic_data)

missing_speed = np.random.choice(n_traffic, size=int(0.03 * n_traffic), replace=False)
df.loc[missing_speed, "avg_speed_kmh"] = None

inconsistent_congestion = np.random.choice(
    n_traffic, size=int(0.02 * n_traffic), replace=False
)
df.loc[inconsistent_congestion, "congestion_level"] = "unknown"

output_path = os.path.join(output_dir, "traffic.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_traffic} traffic records with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing avg_speed: {len(missing_speed)} ({100 * len(missing_speed) / n_traffic:.2f}%)"
)
print(
    f"- Inconsistent congestion_level: {len(inconsistent_congestion)} ({100 * len(inconsistent_congestion) / n_traffic:.2f}%)"
)
print(f"\nCongestion level distribution:")
print(df["congestion_level"].value_counts())
