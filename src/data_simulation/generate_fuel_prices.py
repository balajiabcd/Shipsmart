import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(57)
random.seed(57)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 10000

cities = [
    "Berlin",
    "Munich",
    "Hamburg",
    "Frankfurt",
    "Stuttgart",
    "Cologne",
    "Dusseldorf",
    "Dortmund",
    "Leipzig",
    "Dresden",
]
fuel_types = ["diesel", "petrol", "e5", "e10", "electric"]

fuel_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_records):
    city = random.choice(cities)
    date = base_date + timedelta(days=random.randint(0, 730))
    fuel_type = random.choice(fuel_types)

    if fuel_type == "electric":
        price = random.uniform(0.20, 0.50)
    else:
        price = random.uniform(1.20, 2.20)

    fuel_data.append(
        {
            "date": date.strftime("%Y-%m-%d"),
            "location": city,
            "fuel_type": fuel_type,
            "price_per_liter": round(price, 3),
            "station_brand": random.choice(
                ["Shell", "BP", "Aral", "Total", "Rewe", "EDEKA"]
            ),
        }
    )

df = pd.DataFrame(fuel_data)

outlier_prices = np.random.choice(n_records, size=int(0.02 * n_records), replace=False)
df.loc[outlier_prices, "price_per_liter"] = (
    df.loc[outlier_prices, "price_per_liter"] * 3
)

output_path = os.path.join(output_dir, "fuel_prices.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} fuel price records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Outlier prices: {len(outlier_prices)} ({100 * len(outlier_prices) / n_records:.2f}%)"
)
print(f"\nFuel type distribution:")
print(df["fuel_type"].value_counts())
