import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(50)
random.seed(50)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_holidays = 500

german_holidays = [
    ("New Year's Day", "national"),
    ("Epiphany", "regional"),
    ("Good Friday", "movable"),
    ("Easter Monday", "movable"),
    ("Labour Day", "national"),
    ("Ascension Day", "movable"),
    ("Whit Monday", "movable"),
    ("German Unity Day", "national"),
    ("Christmas Day", "national"),
    ("Boxing Day", "national"),
    ("New Year's Eve", "observance"),
    ("St. Martin's Day", "regional"),
    ("Day of Unity", "regional"),
]

regions = [
    "Berlin",
    "Bavaria",
    "Baden-Württemberg",
    "North Rhine-Westphalia",
    "Hamburg",
    "Lower Saxony",
    "Saxony",
    "Schleswig-Holstein",
    "Brandenburg",
    "Thuringia",
]
states = {
    "Berlin": "Berlin",
    "Bavaria": "Bayern",
    "Baden-Württemberg": "Baden-Württemberg",
    "North Rhine-Westphalia": "NRW",
    "Hamburg": "Hamburg",
}

holiday_data = []
base_year = datetime.now().year - 2

for i in range(n_holidays):
    holiday_name, holiday_type = random.choice(german_holidays)
    year = random.choice([base_year, base_year + 1, base_year + 2, base_year + 3])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dt = datetime(year, month, day)
    region = random.choice(regions)

    if random.random() < 0.03:
        date_str = dt.strftime("%d/%m/%Y")
    elif random.random() < 0.03:
        date_str = dt.strftime("%m/%d/%Y")
    else:
        date_str = dt.strftime("%Y-%m-%d")

    holiday_data.append(
        {
            "date": date_str,
            "country": "Germany",
            "region": region,
            "holiday_name": holiday_name,
            "holiday_type": holiday_type,
            "celebrations_expected": random.randint(1000, 100000),
        }
    )

df = pd.DataFrame(holiday_data)

missing_region = np.random.choice(
    n_holidays, size=int(0.05 * n_holidays), replace=False
)
df.loc[missing_region, "region"] = None

duplicate_indices = np.random.choice(n_holidays, size=10, replace=False)
source_indices = np.random.choice(n_holidays, size=10, replace=True)
for idx, src_idx in zip(duplicate_indices, source_indices):
    df.loc[idx, "holiday_name"] = df.loc[src_idx, "holiday_name"]

output_path = os.path.join(output_dir, "holidays.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_holidays} holiday records with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing region: {len(missing_region)} ({100 * len(missing_region) / n_holidays:.2f}%)"
)
print(f"- Inconsistent date formats: ~6%")
print(f"- Duplicate holidays: 10")
print(f"\nHoliday type distribution:")
print(df["holiday_type"].value_counts())
