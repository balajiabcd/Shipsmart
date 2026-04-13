import pandas as pd
import numpy as np
import random
import os

np.random.seed(47)
random.seed(47)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_locations = 500

german_cities = {
    "Berlin": (52.52, 13.405, "East", 3645000),
    "Munich": (48.1351, 11.582, "South", 1471000),
    "Hamburg": (53.5511, 9.9937, "North", 1841000),
    "Frankfurt": (50.1109, 8.6821, "West", 753000),
    "Stuttgart": (48.7758, 9.1829, "South", 632000),
    "Cologne": (50.9375, 6.9603, "West", 1086000),
    "Dusseldorf": (51.2277, 6.7735, "West", 619000),
    "Dortmund": (51.5136, 7.4653, "West", 588000),
    "Leipzig": (51.3397, 12.3731, "East", 593000),
    "Dresden": (51.0504, 13.7373, "East", 556000),
    "Nuremberg": (49.4542, 11.0775, "South", 518000),
    "Hannover": (52.3759, 9.7320, "North", 538000),
    "Bonn": (50.7379, 7.1762, "West", 328000),
    "Mannheim": (49.4875, 8.4660, "West", 309000),
    "Munster": (51.9607, 7.6271, "West", 314000),
    "Karlsruhe": (49.0069, 8.4037, "South", 312000),
    "Augsburg": (48.3705, 10.8978, "South", 295000),
    "Wuppertal": (51.2562, 7.1509, "West", 355000),
    "Bielefeld": (52.0302, 8.5323, "West", 334000),
    "Münchengladbach": (51.1805, 6.4428, "West", 262000),
}

regions = ["North", "South", "East", "West", "Central"]

location_data = []
for i in range(n_locations):
    base_city = random.choice(list(german_cities.keys()))
    lat, lon, region, pop = german_cities[base_city]

    lat += random.uniform(-0.1, 0.1)
    lon += random.uniform(-0.1, 0.1)

    location_data.append(
        {
            "location_id": f"LOC-{str(i + 1).zfill(4)}",
            "city": base_city,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "region": np.random.choice(regions),
            "population": int(pop * random.uniform(0.1, 3.0)),
            "location_type": np.random.choice(
                ["residential", "commercial", "industrial"]
            ),
            "postal_code": f"{random.randint(10000, 99999)}",
        }
    )

df = pd.DataFrame(location_data)

missing_coords = np.random.choice(
    n_locations, size=int(0.02 * n_locations), replace=False
)
df.loc[missing_coords[:10], "latitude"] = None
df.loc[missing_coords[:10], "longitude"] = None

geocoding_issues = np.random.choice(
    n_locations, size=int(0.05 * n_locations), replace=False
)
df.loc[geocoding_issues, "latitude"] = df.loc[
    geocoding_issues, "latitude"
] * random.uniform(1.1, 1.3)
df.loc[geocoding_issues, "longitude"] = df.loc[
    geocoding_issues, "longitude"
] * random.uniform(1.1, 1.3)

output_path = os.path.join(output_dir, "locations.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_locations} locations with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing coordinates: {len(missing_coords)} ({100 * len(missing_coords) / n_locations:.2f}%)"
)
print(
    f"- Geocoding issues: {len(geocoding_issues)} ({100 * len(geocoding_issues) / n_locations:.2f}%)"
)
print(f"\nLocation type distribution:")
print(df["location_type"].value_counts())
