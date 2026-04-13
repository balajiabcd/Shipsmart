import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(56)
random.seed(56)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 5000

vehicle_ids = [f"VEH-{str(i).zfill(3)}" for i in range(1, 301)]
maintenance_types = [
    "oil_change",
    "tire_rotation",
    "brake_service",
    "inspection",
    "repair",
    "replacement",
    "general_check",
]

maintenance_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_records):
    vehicle = random.choice(vehicle_ids)
    date = base_date + timedelta(days=random.randint(0, 730))
    maint_type = random.choice(maintenance_types)
    cost = random.uniform(50, 2000)

    maintenance_data.append(
        {
            "vehicle_id": vehicle,
            "maintenance_date": date.strftime("%Y-%m-%d"),
            "maintenance_type": maint_type,
            "cost": round(cost, 2),
            "description": f"{maint_type.replace('_', ' ').title()} - {random.choice(['routine', 'scheduled', 'emergency', 'preventive'])}",
            "mechanic_id": f"MECH-{random.randint(1, 20)}",
            "mileage_at_service": random.randint(10000, 200000),
            "next_maintenance_due": (
                date + timedelta(days=random.randint(30, 365))
            ).strftime("%Y-%m-%d"),
            "service_duration_hours": round(random.uniform(1, 24), 1),
        }
    )

df = pd.DataFrame(maintenance_data)

missing_next_due = np.random.choice(
    n_records, size=int(0.05 * n_records), replace=False
)
df.loc[missing_next_due, "next_maintenance_due"] = None

random_gaps = np.random.choice(n_records, size=int(0.03 * n_records), replace=False)
df.loc[random_gaps, "description"] = None

output_path = os.path.join(output_dir, "vehicle_maintenance.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} vehicle maintenance records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing next_maintenance_due: {len(missing_next_due)} ({100 * len(missing_next_due) / n_records:.2f}%)"
)
print(f"- Random gaps: {len(random_gaps)} ({100 * len(random_gaps) / n_records:.2f}%)")
print(f"\nMaintenance type distribution:")
print(df["maintenance_type"].value_counts())
