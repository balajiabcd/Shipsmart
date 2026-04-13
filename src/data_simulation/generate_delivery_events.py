import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(52)
random.seed(52)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_events = 200000

event_types = [
    "created",
    "picked_up",
    "in_transit",
    "out_for_delivery",
    "delivered",
    "failed_attempt",
]
order_ids = [f"ORD-{str(i).zfill(8)}" for i in range(1, 100001)]
location_ids = [f"LOC-{str(i).zfill(4)}" for i in range(1, 501)]

event_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_events):
    order = random.choice(order_ids)
    event_type = random.choice(event_types)
    timestamp = base_date + timedelta(
        days=random.randint(0, 730),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    location = random.choice(location_ids)

    event_data.append(
        {
            "event_id": f"EVT-{str(i + 1).zfill(8)}",
            "order_id": order,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "location_id": location,
            "driver_id": f"DRV-{str(random.randint(1, 500)).zfill(4)}"
            if event_type not in ["created"]
            else None,
            "notes": random.choice(
                [
                    None,
                    "Left at door",
                    "Neighbor received",
                    "Business closed",
                    "Wrong address",
                ]
            ),
        }
    )

df = pd.DataFrame(event_data)

missing_timestamp = np.random.choice(n_events, size=int(0.03 * n_events), replace=False)
df.loc[missing_timestamp, "timestamp"] = None

missing_location = np.random.choice(n_events, size=int(0.01 * n_events), replace=False)
df.loc[missing_location, "location_id"] = None

output_path = os.path.join(output_dir, "delivery_events.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_events} delivery event records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing timestamp: {len(missing_timestamp)} ({100 * len(missing_timestamp) / n_events:.2f}%)"
)
print(
    f"- Missing location_id: {len(missing_location)} ({100 * len(missing_location) / n_events:.2f}%)"
)
print(f"\nEvent type distribution:")
print(df["event_type"].value_counts())
