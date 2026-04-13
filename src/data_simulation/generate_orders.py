import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_orders = 100000

order_ids = [f"ORD-{str(i).zfill(8)}" for i in range(1, n_orders + 1)]
customer_ids = [
    f"CUST-{str(i).zfill(6)}" for i in np.random.randint(1, 20001, n_orders)
]
driver_ids = [f"DRV-{str(i).zfill(4)}" for i in np.random.randint(1, 501, n_orders)]
warehouse_ids = [f"WH-{str(i).zfill(2)}" for i in np.random.randint(1, 21, n_orders)]

cities = {
    "Berlin": (52.52, 13.405),
    "Munich": (48.1351, 11.582),
    "Hamburg": (53.5511, 9.9937),
    "Frankfurt": (50.1109, 8.6821),
    "Stuttgart": (48.7758, 9.1829),
    "Cologne": (50.9375, 6.9603),
    "Dusseldorf": (51.2277, 6.7735),
    "Dortmund": (51.5136, 7.4653),
    "Leipzig": (51.3397, 12.3731),
    "Dresden": (51.0504, 13.7373),
    "Nuremberg": (49.4542, 11.0775),
    "Hannover": (52.3759, 9.7320),
    "Bonn": (50.7379, 7.1762),
    "Mannheim": (49.4875, 8.4660),
    "Munster": (51.9607, 7.6271),
}

origins = []
destinations = []
for _ in range(n_orders):
    origin_city = random.choice(list(cities.keys()))
    dest_city = random.choice(list(cities.keys()))
    while dest_city == origin_city:
        dest_city = random.choice(list(cities.keys()))
    origins.append(cities[origin_city])
    destinations.append(cities[dest_city])

base_date = datetime.now() - timedelta(days=730)
order_times = [
    base_date
    + timedelta(
        days=random.randint(0, 730),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    for _ in range(n_orders)
]

delivery_promises = [ot + timedelta(hours=random.randint(24, 72)) for ot in order_times]

statuses = np.random.choice(
    ["delivered", "in_transit", "pending", "cancelled"],
    n_orders,
    p=[0.82, 0.12, 0.04, 0.02],
)

actual_deliveries = []
delay_minutes = []
for i, status in enumerate(statuses):
    if status == "delivered":
        if random.random() < 0.12:
            delay = random.randint(5, 240)
            delay_minutes.append(delay)
            actual_deliveries.append(delivery_promises[i] + timedelta(minutes=delay))
        else:
            delay_minutes.append(0)
            actual_deliveries.append(
                delivery_promises[i] + timedelta(minutes=random.randint(-15, 15))
            )
    else:
        delay_minutes.append(None)
        actual_deliveries.append(None)

df = pd.DataFrame(
    {
        "order_id": order_ids,
        "customer_id": customer_ids,
        "driver_id": driver_ids,
        "warehouse_id": warehouse_ids,
        "origin_location": [o[0] for o in origins],
        "origin_longitude": [o[1] for o in origins],
        "dest_location": [d[0] for d in destinations],
        "dest_longitude": [d[1] for d in destinations],
        "order_time": order_times,
        "scheduled_delivery_time": delivery_promises,
        "actual_delivery_time": actual_deliveries,
        "status": statuses,
        "delay_minutes": delay_minutes,
        "package_weight_kg": np.random.uniform(0.1, 100, n_orders).round(2),
        "package_dimensions_length_cm": np.random.randint(10, 100, n_orders),
        "package_dimensions_width_cm": np.random.randint(10, 80, n_orders),
        "package_dimensions_height_cm": np.random.randint(5, 60, n_orders),
        "package_type": np.random.choice(
            ["document", "parcel", "fragile", "oversized", "electronics"],
            n_orders,
            p=[0.4, 0.35, 0.15, 0.07, 0.03],
        ),
        "shipping_type": np.random.choice(
            ["standard", "express", "overnight"], n_orders, p=[0.70, 0.25, 0.05]
        ),
        "priority": np.random.choice(
            ["low", "medium", "high", "urgent"], n_orders, p=[0.50, 0.35, 0.12, 0.03]
        ),
        "estimated_cost_eur": np.random.uniform(5.0, 500.0, n_orders).round(2),
        "actual_cost_eur": np.random.uniform(5.0, 500.0, n_orders).round(2),
    }
)

missing_mask = np.random.random(n_orders)
df.loc[missing_mask < 0.03, "driver_id"] = None
missing_mask = np.random.random(n_orders)
df.loc[missing_mask < 0.03, "warehouse_id"] = None
missing_mask = np.random.random(n_orders)
df.loc[missing_mask < 0.02, "package_weight_kg"] = None

outlier_mask = np.random.random(n_orders) < 0.02
df.loc[outlier_mask, "package_weight_kg"] = (
    df.loc[outlier_mask, "package_weight_kg"] * 10
)

invalid_date_mask = np.random.random(n_orders) < 0.01
df["order_time"] = df["order_time"].astype(object)
df.loc[invalid_date_mask, "order_time"] = "invalid_date"

duplicate_indices = np.random.choice(n_orders, size=1500, replace=False)
source_indices = np.random.choice(n_orders, size=1500, replace=True)
df.loc[duplicate_indices, "order_id"] = df.iloc[source_indices]["order_id"].values

output_path = os.path.join(output_dir, "orders.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_orders} orders with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing driver_id: {df['driver_id'].isna().sum()} ({100 * df['driver_id'].isna().sum() / n_orders:.2f}%)"
)
print(
    f"- Missing warehouse_id: {df['warehouse_id'].isna().sum()} ({100 * df['warehouse_id'].isna().sum() / n_orders:.2f}%)"
)
print(
    f"- Missing package_weight: {df['package_weight_kg'].isna().sum()} ({100 * df['package_weight_kg'].isna().sum() / n_orders:.2f}%)"
)
print(
    f"- Delayed orders: {df[df['delay_minutes'].notna() & (df['delay_minutes'] > 0)].shape[0]} ({100 * df[df['delay_minutes'].notna() & (df['delay_minutes'] > 0)].shape[0] / n_orders:.2f}%)"
)
print(f"\nStatus distribution:")
print(df["status"].value_counts())
