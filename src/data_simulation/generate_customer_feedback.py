import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(58)
random.seed(58)

output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

n_records = 30000

order_ids = [f"ORD-{str(i).zfill(8)}" for i in range(1, 100001)]
customer_ids = [f"CUST-{str(i).zfill(5)}" for i in range(1, 20001)]
comments = [
    "Great delivery!",
    "Very fast",
    "Package damaged",
    "On time",
    "Late delivery",
    "Excellent service",
    "Good",
    "Could be better",
    "Not happy",
    "Recommended!",
    "Would order again",
    None,
    None,
    None,
    None,
    None,
]

feedback_data = []
base_date = datetime.now() - timedelta(days=730)

for i in range(n_records):
    order = random.choice(order_ids)
    customer = random.choice(customer_ids)
    date = base_date + timedelta(
        days=random.randint(0, 730), hours=random.randint(0, 23)
    )

    feedback_data.append(
        {
            "feedback_id": f"FD-{str(i + 1).zfill(8)}",
            "order_id": order,
            "customer_id": customer,
            "rating": random.randint(1, 5),
            "comment": random.choice(comments),
            "feedback_date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "feedback_type": random.choice(["delivery", "packaging", "service"]),
            "would_recommend": random.choice([True, False]),
        }
    )

df = pd.DataFrame(feedback_data)

missing_timestamp = np.random.choice(
    n_records, size=int(0.02 * n_records), replace=False
)
df.loc[missing_timestamp, "feedback_date"] = None

output_path = os.path.join(output_dir, "customer_feedback.csv")
df.to_csv(output_path, index=False)

print(f"Generated {n_records} customer feedback records")
print(f"Saved to: {output_path}")
print(f"\nData Quality Summary:")
print(f"- Missing comments: ~{int(0.4 * n_records)} (40%)")
print(
    f"- Missing timestamps: {len(missing_timestamp)} ({100 * len(missing_timestamp) / n_records:.2f}%)"
)
print(f"\nRating distribution:")
print(df["rating"].value_counts().sort_index())
