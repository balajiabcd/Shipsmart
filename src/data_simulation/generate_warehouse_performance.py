import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(54)
random.seed(54)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 5000

warehouse_ids = [f"WH-{str(i).zfill(2)}" for i in range(1, 21)]

performance_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_records):
    warehouse = random.choice(warehouse_ids)
    date = base_date + timedelta(days=random.randint(0, 730))

    throughput = random.randint(100, 800)
    avg_processing = random.uniform(10, 45)
    delays = random.randint(0, 20)
    efficiency = random.uniform(70, 98)

    performance_data.append(
        {
            "warehouse_id": warehouse,
            "date": date.strftime("%Y-%m-%d"),
            "inbound_volume": random.randint(50, 400),
            "outbound_volume": throughput,
            "throughput": throughput,
            "avg_processing_time_minutes": round(avg_processing, 2),
            "delays_count": delays,
            "efficiency_score": round(efficiency, 2),
            "staff_count": random.randint(10, 100),
            "overtime_hours": round(random.uniform(0, 100), 1),
            "error_rate": round(random.uniform(0, 5), 2),
            "returns_received": random.randint(0, 50),
        }
    )

df = pd.DataFrame(performance_data)

missing_efficiency = np.random.choice(
    n_records, size=int(0.10 * n_records), replace=False
)
df.loc[missing_efficiency, "efficiency_score"] = None

outlier_throughput = np.random.choice(
    n_records, size=int(0.03 * n_records), replace=False
)
df.loc[outlier_throughput, "throughput"] = df.loc[outlier_throughput, "throughput"] * 5

output_path = os.path.join(output_dir, "warehouse_performance.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} warehouse performance records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing efficiency: {len(missing_efficiency)} ({100 * len(missing_efficiency) / n_records:.2f}%)"
)
print(
    f"- Outlier throughput: {len(outlier_throughput)} ({100 * len(outlier_throughput) / n_records:.2f}%)"
)
print(f"\nEfficiency score stats:")
print(df["efficiency_score"].describe())
