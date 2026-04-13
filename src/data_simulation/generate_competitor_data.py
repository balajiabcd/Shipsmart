import pandas as pd
import numpy as np
import random
import os

np.random.seed(59)
random.seed(59)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 1000

competitors = [
    "DHL",
    "UPS",
    "FedEx",
    "DPD",
    "Hermes",
    "GLS",
    "DB Schenker",
    "Kuehne+Nagel",
    "DSV",
    "Schenker",
    "Transporeon",
    "Freightos",
    "Flexport",
    "Coyote",
    "C.H. Robinson",
]

regions = ["North", "South", "East", "West", "Central", "Nationwide"]
pricing_tiers = ["budget", "standard", "premium"]

competitor_data = []

for i in range(n_records):
    comp = random.choice(competitors)
    region = random.choice(regions)

    competitor_data.append(
        {
            "competitor_id": f"COMP-{str(i + 1).zfill(3)}",
            "competitor_name": comp,
            "region": region,
            "market_share_percent": round(random.uniform(1, 25), 2),
            "avg_delivery_time_days": round(random.uniform(1, 7), 1),
            "pricing_tier": random.choice(pricing_tiers),
            "service_rating": round(random.uniform(2.5, 5.0), 2),
            "coverage_cities": random.randint(10, 500),
            "data_date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        }
    )

df = pd.DataFrame(competitor_data)

missing_share = np.random.choice(n_records, size=int(0.10 * n_records), replace=False)
df.loc[missing_share, "market_share_percent"] = None

output_path = os.path.join(output_dir, "competitor_data.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} competitor data records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing market_share: {len(missing_share)} ({100 * len(missing_share) / n_records:.2f}%)"
)
print(f"\nCompetitor distribution:")
print(df["competitor_name"].value_counts())
