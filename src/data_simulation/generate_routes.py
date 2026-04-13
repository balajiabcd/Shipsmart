import pandas as pd
import numpy as np
import random
import os

np.random.seed(46)
random.seed(46)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_routes = 1000

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
    "Nuremberg",
    "Hannover",
    "Bonn",
    "Mannheim",
    "Munster",
    "Karlsruhe",
    "Augsburg",
    "Wuppertal",
    "Bielefeld",
    "Münchengladbach",
]

route_types = ["highway", "secondary", "local", "mixed", "urban"]
traffic_levels = ["low", "medium", "high"]

route_data = []
for i in range(n_routes):
    origin = random.choice(cities)
    dest = random.choice(cities)
    while dest == origin:
        dest = random.choice(cities)

    dist_km = random.uniform(10, 800)
    avg_duration = int(dist_km / random.uniform(60, 120) * 60)
    rt = np.random.choice(route_types)
    tl = np.random.choice(traffic_levels, p=[0.3, 0.45, 0.25])

    route_data.append(
        {
            "route_id": f"RTE-{str(i + 1).zfill(4)}",
            "origin_city": origin,
            "destination_city": dest,
            "distance_km": round(dist_km, 2),
            "avg_duration_minutes": avg_duration,
            "route_type": rt,
            "traffic_level": tl,
            "toll_roads": random.choice([True, False]),
            "preferred_times": random.choice(
                ["morning", "afternoon", "evening", "any"]
            ),
        }
    )

df = pd.DataFrame(route_data)

missing_duration_indices = np.random.choice(
    n_routes, size=int(0.05 * n_routes), replace=False
)
df.loc[missing_duration_indices, "avg_duration_minutes"] = None

duplicate_indices = np.random.choice(n_routes, size=15, replace=False)
for idx in duplicate_indices:
    source_idx = random.randint(0, n_routes - 1)
    df.loc[idx, "origin_city"] = df.loc[source_idx, "origin_city"]
    df.loc[idx, "destination_city"] = df.loc[source_idx, "destination_city"]

inconsistent_type_indices = np.random.choice(
    n_routes, size=int(0.02 * n_routes), replace=False
)
df.loc[inconsistent_type_indices, "route_type"] = "unknown"

output_path = os.path.join(output_dir, "routes.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_routes} routes with intentional errors")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(
    f"- Missing avg_duration: {len(missing_duration_indices)} ({100 * len(missing_duration_indices) / n_routes:.2f}%)"
)
print(f"- Duplicate origin/dest: 15")
print(
    f"- Inconsistent route_type: {len(inconsistent_type_indices)} ({100 * len(inconsistent_type_indices) / n_routes:.2f}%)"
)
print(f"\nRoute type distribution:")
print(df["route_type"].value_counts())
