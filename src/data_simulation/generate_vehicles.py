import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(44)
random.seed(44)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_vehicles = 300

vehicle_types = ["van", "truck", "motorcycle", "scooter", "car"]
makes_models = {
    "van": [
        ("Mercedes", "Sprinter"),
        ("Ford", "Transit"),
        ("Renault", "Master"),
        ("Iveco", "Daily"),
    ],
    "truck": [
        ("MAN", "TGS"),
        ("Mercedes", "Actros"),
        ("Scania", "R450"),
        ("Volvo", "FH"),
    ],
    "motorcycle": [("BMW", "R1200"), ("Honda", "CTX700"), ("Yamaha", "XT1200Z")],
    "scooter": [("Piaggio", "Liberty"), ("Vespa", "LX125"), ("Honda", "PCX125")],
    "car": [("VW", "Caddy"), ("Opel", "Movano"), ("Peugeot", "Boxer")],
}


def generate_plate():
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    idx1 = random.randint(0, len(letters) - 1)
    idx2 = random.randint(0, len(letters) - 1)
    if random.random() < 0.7:
        return f"B-{random.randint(1, 99)}-{letters[idx1]}{letters[idx2]}{random.randint(100, 999)}"
    else:
        idx3 = random.randint(0, 3)
        return f"{letters[idx3]}{letters[idx1]} {random.randint(1, 999)}"


vehicle_ids = [f"VEH-{str(i).zfill(3)}" for i in range(1, n_vehicles + 1)]
v_types = np.random.choice(vehicle_types, n_vehicles, p=[0.40, 0.25, 0.15, 0.10, 0.10])
makes_list = []
models_list = []
for vt in v_types:
    mm = random.choice(makes_models[vt])
    makes_list.append(mm[0])
    models_list.append(mm[1])

years = np.random.randint(2015, 2025, n_vehicles)

capacities = []
for vt in v_types:
    if vt == "van":
        capacities.append(random.uniform(500, 1500))
    elif vt == "truck":
        capacities.append(random.uniform(2000, 10000))
    elif vt == "motorcycle":
        capacities.append(random.uniform(50, 200))
    elif vt == "scooter":
        capacities.append(random.uniform(20, 100))
    else:
        capacities.append(random.uniform(100, 500))
capacities = [round(c, 2) for c in capacities]

plate_numbers = [generate_plate() for _ in range(n_vehicles)]
vins = [
    f"WDR{random.randint(1000000000000000, 9999999999999999)}"
    for _ in range(n_vehicles)
]

maintenance_due = []
for _ in range(n_vehicles):
    days_ahead = random.randint(-90, 180)
    maintenance_due.append(
        (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    )

insurance_expiry = []
for _ in range(n_vehicles):
    days_ahead = random.randint(30, 730)
    insurance_expiry.append(
        (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    )

statuses = np.random.choice(
    ["active", "maintenance", "retired"], n_vehicles, p=[0.85, 0.10, 0.05]
)

mileages = np.random.randint(10000, 250000, n_vehicles)
fuel_types = np.random.choice(
    ["diesel", "petrol", "electric", "hybrid"], n_vehicles, p=[0.65, 0.25, 0.07, 0.03]
)

df = pd.DataFrame(
    {
        "vehicle_id": vehicle_ids,
        "vehicle_type": v_types,
        "make": makes_list,
        "model": models_list,
        "manufacturing_year": years,
        "capacity_kg": capacities,
        "plate_number": plate_numbers,
        "vin": vins,
        "insurance_expiry": insurance_expiry,
        "maintenance_due": maintenance_due,
        "status": statuses,
        "mileage": mileages,
        "fuel_type": fuel_types,
    }
)

outlier_mask = np.random.random(n_vehicles) < 0.02
df.loc[outlier_mask, "capacity_kg"] = df.loc[outlier_mask, "capacity_kg"] * 10

missing_maintenance = np.random.random(n_vehicles) < 0.05
df.loc[missing_maintenance, "maintenance_due"] = None

duplicate_plates = np.random.choice(n_vehicles, size=3, replace=False)
for idx in duplicate_plates:
    source_idx = random.randint(0, n_vehicles - 1)
    df.loc[idx, "plate_number"] = df.loc[source_idx, "plate_number"]

output_path = os.path.join(output_dir, "vehicles.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_vehicles} vehicles with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Outlier capacity (10x): {outlier_mask.sum()} ({100 * outlier_mask.sum() / n_vehicles:.2f}%)"
)
print(
    f"- Missing maintenance_due: {missing_maintenance.sum()} ({100 * missing_maintenance.sum() / n_vehicles:.2f}%)"
)
print(f"- Duplicate plates: 3")
print(f"\nStatus distribution:")
print(df["status"].value_counts())
