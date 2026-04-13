import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(51)
random.seed(51)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_customers = 20000

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
]

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

customer_data = []

for i in range(n_customers):
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@example.com"

    phone = f"+49{random.randint(30, 89)}{random.randint(1000000, 9999999)}"

    city = random.choice(cities)
    street = f"{random.choice(['Haupt', 'Berg', 'Wald', 'See', 'Kirch', 'Schloss', 'Markt', 'Bahn', 'Garten', 'Friedrich'])}str. {random.randint(1, 99)}"

    start = datetime(2018, 1, 1)
    end = datetime(2024, 12, 31)
    delta = end - start
    reg_date = start + timedelta(days=random.randint(0, delta.days))

    customer_data.append(
        {
            "customer_id": f"CUST-{str(i + 1).zfill(5)}",
            "first_name": first,
            "last_name": last,
            "email": email,
            "phone": phone,
            "street_address": street,
            "city": city,
            "postal_code": f"{random.randint(10000, 99999)}",
            "customer_since": reg_date.strftime("%Y-%m-%d"),
            "customer_type": random.choice(["individual", "business"]),
            "credit_limit": random.randint(100, 5000),
            "preferred_shipping": random.choice(["standard", "express"]),
            "account_status": random.choice(["active", "active", "active", "inactive"]),
        }
    )

df = pd.DataFrame(customer_data)

duplicate_emails = np.random.choice(
    n_customers, size=int(0.02 * n_customers), replace=False
)
source_indices = np.random.choice(
    n_customers, size=int(0.02 * n_customers), replace=True
)
for idx, src_idx in zip(duplicate_emails, source_indices):
    df.loc[idx, "email"] = df.loc[src_idx, "email"]

missing_phone = np.random.choice(
    n_customers, size=int(0.03 * n_customers), replace=False
)
df.loc[missing_phone, "phone"] = None

output_path = os.path.join(output_dir, "customers.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_customers} customer records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Notes (PII WARNING):")
print(f"- Real PII-like data included (names, emails, phones)")
print(
    f"- Duplicate emails: {len(duplicate_emails)} ({100 * len(duplicate_emails) / n_customers:.2f}%)"
)
print(f"- NOTE: Handle PII according to GDPR in production")
print(f"\nCustomer type distribution:")
print(df["customer_type"].value_counts())
