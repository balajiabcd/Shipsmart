import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(53)
random.seed(53)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 50000

driver_ids = [f"DRV-{str(i).zfill(4)}" for i in range(1, 501)]

performance_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_records):
    driver = random.choice(driver_ids)
    date = base_date + timedelta(days=random.randint(0, 730))

    total_deliveries = random.randint(5, 40)
    on_time = (
        random.randint(3, total_deliveries - 1)
        if random.random() > 0.1
        else random.randint(0, total_deliveries)
    )
    late = total_deliveries - on_time if total_deliveries >= on_time else 0
    rating = random.uniform(2.5, 5.0)

    performance_data.append(
        {
            "driver_id": driver,
            "date": date.strftime("%Y-%m-%d"),
            "total_deliveries": total_deliveries,
            "on_time_deliveries": on_time,
            "late_deliveries": late,
            "rating": round(rating, 2),
            "customer_complaints": random.randint(0, 5),
            "fuel_efficiency": round(random.uniform(6, 20), 2),
            "accidents": random.randint(0, 3),
            "overtime_hours": round(random.uniform(0, 8), 1),
        }
    )

df = pd.DataFrame(performance_data)

missing_rating = np.random.choice(n_records, size=int(0.05 * n_records), replace=False)
df.loc[missing_rating, "rating"] = None

missing_complaints = np.random.choice(
    n_records, size=int(0.02 * n_records), replace=False
)
df.loc[missing_complaints, "customer_complaints"] = None

output_path = os.path.join(output_dir, "drivers_performance.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} driver performance records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing rating: {len(missing_rating)} ({100 * len(missing_rating) / n_records:.2f}%)"
)
print(
    f"- Missing complaints: {len(missing_complaints)} ({100 * len(missing_complaints) / n_records:.2f}%)"
)
print(f"\nRating stats:")
print(df["rating"].describe())
