import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(45)
random.seed(45)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_warehouses = 20

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
    "Karlsruhe": (49.0069, 8.4037),
    "Augsburg": (48.3705, 10.8978),
    "Wuppertal": (51.2562, 7.1509),
    "Bielefeld": (52.0302, 8.5323),
    "Münchengladbach": (51.1805, 6.4428),
}

first_names = [
    "Hans",
    "Klaus",
    "Peter",
    "Wolfgang",
    "Thomas",
    "Stefan",
    "Michael",
    "Christian",
    "Frank",
    "Andreas",
    "Julia",
    "Anna",
    "Maria",
    "Sandra",
    "Nicole",
]
last_names = [
    "Müller",
    "Schmidt",
    "Schneider",
    "Fischer",
    "Weber",
    "Hoffmann",
    "Schäfer",
    "Koch",
    "Bauer",
    "Richter",
    "Klein",
    "Wolf",
    "Schröder",
    "Neumann",
    "Schwarz",
]

warehouse_ids = [f"WH-{str(i).zfill(2)}" for i in range(1, n_warehouses + 1)]
names = [f"{city} Hub" for city in cities.keys()]
lats = [cities[c][0] for c in cities.keys()]
lons = [cities[c][1] for c in cities.keys()]
capacities = np.random.randint(5000, 25000, n_warehouses)

manager_names = [
    f"{random.choice(first_names)} {random.choice(last_names)}"
    for _ in range(n_warehouses)
]
contact_phones = [
    f"+49{random.randint(30, 89)}{random.randint(1000000, 9999999)}"
    for _ in range(n_warehouses)
]
emails = [f"warehouse{i + 1}@shipsmart.de" for i in range(n_warehouses)]

established_dates = []
for _ in range(n_warehouses):
    start = datetime(2015, 1, 1)
    end = datetime(2023, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    established_dates.append((start + timedelta(days=random_days)).strftime("%Y-%m-%d"))

operating_hours = np.random.choice(
    ["06:00-22:00", "00:00-24:00", "08:00-20:00", "24/7"],
    n_warehouses,
    p=[0.5, 0.2, 0.2, 0.1],
)
zones = np.random.choice(["A", "B", "C"], n_warehouses, p=[0.4, 0.35, 0.25])
regions = np.random.choice(["North", "South", "East", "West", "Central"], n_warehouses)
statuses = np.random.choice(
    ["active", "expansion", "closed"], n_warehouses, p=[0.85, 0.10, 0.05]
)

df = pd.DataFrame(
    {
        "warehouse_id": warehouse_ids,
        "warehouse_name": names,
        "city": list(cities.keys()),
        "latitude": lats,
        "longitude": lons,
        "capacity_sqm": capacities,
        "manager_name": manager_names,
        "manager_contact": contact_phones,
        "email": emails,
        "established_date": established_dates,
        "operating_hours": operating_hours,
        "zone": zones,
        "region": regions,
        "status": statuses,
    }
)

missing_manager = np.random.random(n_warehouses) < 0.05
df.loc[missing_manager, "manager_name"] = None

missing_phone = np.random.random(n_warehouses) < 0.10
df.loc[missing_phone, "manager_contact"] = None

missing_email = np.random.random(n_warehouses) < 0.03
df.loc[missing_email, "email"] = None

duplicate_indices = np.random.choice(n_warehouses, size=2, replace=False)
for idx in duplicate_indices:
    source_idx = random.randint(0, n_warehouses - 1)
    df.loc[idx, "warehouse_name"] = df.loc[source_idx, "warehouse_name"]

output_path = os.path.join(output_dir, "warehouses.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_warehouses} warehouses with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing manager_name: {missing_manager.sum()} ({100 * missing_manager.sum() / n_warehouses:.2f}%)"
)
print(
    f"- Missing manager_contact: {missing_phone.sum()} ({100 * missing_phone.sum() / n_warehouses:.2f}%)"
)
print(
    f"- Missing email: {missing_email.sum()} ({100 * missing_email.sum() / n_warehouses:.2f}%)"
)
print(f"- Duplicate entries: 2")
print(f"\nStatus distribution:")
print(df["status"].value_counts())
