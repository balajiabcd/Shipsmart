import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(43)
random.seed(43)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_drivers = 500

first_names = [
    "Hans",
    "Klaus",
    "Peter",
    "Wolfgang",
    "Martina",
    "Anna",
    "Maria",
    "Thomas",
    "Stefan",
    "Michael",
    "Julia",
    "Sandra",
    "Nicole",
    "Heike",
    "Christian",
    "Frank",
    "Mathias",
    "Andreas",
    "Uwe",
    "Jürgen",
    "Sebastian",
    "Tim",
    "Lars",
    "Marco",
    "Oliver",
    "Jennifer",
    "Sabrina",
    "Jessica",
    "Tina",
    "Michelle",
    "Daniel",
    "Alex",
    "Chris",
    "Jamie",
    "Jordan",
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
    "Zimmermann",
    "Braun",
    "Krüger",
    "Hartmann",
    "Lange",
    "Werner",
    "Schmitz",
    "Köhler",
    "Herrmann",
    "König",
    "Fuchs",
    "Kaiser",
    "Weiß",
    "Peters",
    "Jung",
    "Hahn",
    "Schubert",
    "Vogel",
    "Friedrich",
    "Keller",
    "Günther",
    "Franke",
    "Sauer",
    "Helmut",
    "Heinrich",
    "Gelb",
    "Orange",
]


def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_license_number():
    return f"DL-{random.randint(10000000, 99999999)}"


def random_date(start_year=2010, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def format_date_inconsistent(dt):
    fmt = random.choice([1, 2, 3])
    if fmt == 1:
        return dt.strftime("%Y-%m-%d")
    elif fmt == 2:
        return dt.strftime("%d/%m/%Y")
    else:
        return dt.strftime("%m-%d-%Y")


driver_ids = [f"DRV-{str(i).zfill(4)}" for i in range(1, n_drivers + 1)]
names = [generate_name() for _ in range(n_drivers)]
license_numbers = [generate_license_number() for _ in range(n_drivers)]

hire_dates_raw = [random_date(2018, 2024) for _ in range(n_drivers)]
hire_dates = [
    format_date_inconsistent(d) if random.random() < 0.05 else d.strftime("%Y-%m-%d")
    for d in hire_dates_raw
]

licence_expiry_dates = [
    d + timedelta(days=random.randint(365, 1825)) for d in hire_dates_raw
]
license_expiry = [d.strftime("%Y-%m-%d") for d in licence_expiry_dates]

vehicle_ids = [
    f"VEH-{str(i).zfill(3)}" if random.random() > 0.1 else None
    for i in np.random.randint(1, 301, n_drivers)
]
statuses = np.random.choice(
    ["active", "on_leave", "suspended"], n_drivers, p=[0.88, 0.08, 0.04]
)
ratings = np.random.uniform(2.5, 5.0, n_drivers).round(2)
total_deliveries = np.random.randint(50, 8000, n_drivers)
on_time_rates = np.random.uniform(0.70, 0.98, n_drivers).round(3)

contact_phones = [
    f"+49{random.randint(150, 179)}{random.randint(1000000, 9999999)}"
    for _ in range(n_drivers)
]
contact_phones = [
    p
    if random.random() > 0.01
    else f"0{random.randint(15179, 179999)}{random.randint(100000, 999999)}"
    for p in contact_phones
]

base_locations = [f"WH-{str(i).zfill(2)}" for i in np.random.randint(1, 21, n_drivers)]

df = pd.DataFrame(
    {
        "driver_id": driver_ids,
        "full_name": names,
        "license_number": license_numbers,
        "license_expiry": license_expiry,
        "vehicle_id": vehicle_ids,
        "hire_date": hire_dates,
        "status": statuses,
        "rating": ratings,
        "total_deliveries": total_deliveries,
        "on_time_rate": on_time_rates,
        "contact_phone": contact_phones,
        "base_location": base_locations,
    }
)

missing_mask = np.random.random(n_drivers) < 0.02
df.loc[missing_mask, "license_number"] = None

missing_vehicle = np.random.random(n_drivers) < 0.03
df.loc[missing_vehicle, "vehicle_id"] = None

duplicate_indices = np.random.choice(n_drivers, size=15, replace=False)
for idx in duplicate_indices:
    source_idx = random.randint(0, n_drivers - 1)
    df.loc[idx, "full_name"] = df.loc[source_idx, "full_name"]
    df.loc[idx, "license_number"] = generate_license_number()

output_path = os.path.join(output_dir, "drivers.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_drivers} drivers with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing license_number: {df['license_number'].isna().sum()} ({100 * df['license_number'].isna().sum() / n_drivers:.2f}%)"
)
print(
    f"- Missing vehicle_id: {df['vehicle_id'].isna().sum()} ({100 * df['vehicle_id'].isna().sum() / n_drivers:.2f}%)"
)
print(f"- Inconsistent hire_date formats: ~5%")
print(f"- Duplicate driver names: 15")
print(f"\nStatus distribution:")
print(df["status"].value_counts())
