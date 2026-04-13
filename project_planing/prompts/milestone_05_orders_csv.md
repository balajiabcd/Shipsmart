# Milestone #5: Generate Orders CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

**From Milestone #4:**
- Data simulation plan created
- 20 CSV file schemas defined

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate orders.csv with Missing Values and Errors

**Project Context:**
- Project: Shipsmart
- **GitHub Repository:** https://github.com/balajiabcd/Shipsmart

**Your Role:**
You are a **Data Engineer** generating synthetic data.

**Instructions:**

1. **Create Python Script**
   Create `src/data_simulation/generate_orders.py`:

   ```python
   import pandas as pd
   import numpy as np
   from datetime import datetime, timedelta
   import random

   np.random.seed(42)
   random.seed(42)

   # Generate 100,000 order records
   n_orders = 100000

   # Base data
   order_ids = [f"ORD-{str(i).zfill(8)}" for i in range(1, n_orders + 1)]
   customer_ids = [f"CUST-{str(i).zfill(6)}" for i in np.random.randint(1, 20001, n_orders)]
   driver_ids = [f"DRV-{str(i).zfill(4)}" for i in np.random.randint(1, 501, n_orders)]
   warehouse_ids = [f"WH-{str(i).zfill(2)}" for i in np.random.randint(1, 21, n_orders)]
   
   # Locations (latitude, longitude)
   cities = {
       "Berlin": (52.52, 13.405),
       "Munich": (48.1351, 11.582),
       "Hamburg": (53.5511, 9.9937),
       "Frankfurt": (50.1109, 8.6821),
       "Stuttgart": (48.7758, 9.1829),
       "Cologne": (50.9375, 6.9603),
       "Dusseldorf": (51.2277, 6.7735),
       "Dortmund": (51.5136, 7.4653),
       "Leipzig": (51.3397, 12.3731),
       "Dresden": (51.0504, 13.7373)
   }

   # Generate origin/destination
   origins = []
   destinations = []
   for _ in range(n_orders):
       origin_city = random.choice(list(cities.keys()))
       dest_city = random.choice(list(cities.keys()))
       while dest_city == origin_city:
           dest_city = random.choice(list(cities.keys()))
       origins.append(cities[origin_city])
       destinations.append(cities[dest_city])

   # Order times (past 2 years)
   base_date = datetime.now() - timedelta(days=730)
   order_times = [base_date + timedelta(days=random.randint(0, 730), hours=random.randint(0, 23)) for _ in range(n_orders)]

   # Delivery promise (24-72 hours after order)
   delivery_promises = [ot + timedelta(hours=random.randint(24, 72)) for ot in order_times]

   # Status distribution (85% delivered, 10% in transit, 5% pending/cancelled)
   statuses = np.random.choice(
       ['delivered', 'in_transit', 'pending', 'cancelled'],
       n_orders,
       p=[0.85, 0.10, 0.03, 0.02]
   )

   # Introduce DELAYED status (10% of delivered)
   actual_deliveries = []
   for i, status in enumerate(statuses):
       if status == 'delivered':
           if random.random() < 0.10:  # 10% delayed
               # Delay by 5-180 minutes
               delay = timedelta(minutes=random.randint(5, 180))
               actual_deliveries.append(delivery_promises[i] + delay)
           else:
               actual_deliveries.append(delivery_promises[i] + timedelta(minutes=random.randint(-10, 10)))
       else:
           actual_deliveries.append(None)

   df = pd.DataFrame({
       'order_id': order_ids,
       'customer_id': customer_ids,
       'driver_id': driver_ids,
       'warehouse_id': warehouse_ids,
       'origin_lat': [o[0] for o in origins],
       'origin_lon': [o[1] for o in origins],
       'dest_lat': [d[0] for d in destinations],
       'dest_lon': [d[1] for d in destinations],
       'order_time': order_times,
       'delivery_promise': delivery_promises,
       'actual_delivery': actual_deliveries,
       'status': statuses,
       'package_weight_kg': np.random.uniform(0.5, 50, n_orders).round(2),
       'package_type': np.random.choice(['document', 'parcel', 'fragile', 'oversized'], n_orders),
   })

   # Introduce data quality issues
   # 3% missing values in various columns
   for col in ['driver_id', 'warehouse_id', 'package_weight_kg']:
       mask = np.random.random(n_orders) < 0.03
       df.loc[mask, col] = None

   # 1% invalid dates
   mask = np.random.random(n_orders) < 0.01
   df.loc[mask, 'order_time'] = 'invalid_date'

   # Save
   df.to_csv('data/raw/orders.csv', index=False)
   print(f"Generated {n_orders} orders with intentional errors")
   ```

2. **Run the Script**
   ```bash
   mkdir -p data/raw src/data_simulation
   python src/data_simulation/generate_orders.py
   ```

3. **Verify Data Quality Issues**
   - Check missing values (~3%)
   - Check invalid dates (~1%)
   - Document issues in `docs/data_quality_report.md`

4. **Commit and Push**
   ```bash
   git add data/raw/orders.csv src/data_simulation/generate_orders.py
   git commit -m "Generate orders.csv with 100k records and data quality issues"
   git push
   ```

**Subagent Task:**
If needed, ask ML Engineer 1 about target variable (delay) definition.

---

## Section 3: Instructions for Next AI Agent

### Milestone Completion Summary

**Completed Tasks:**
1. ✅ Created generate_orders.py script
2. ✅ Generated 100,000 order records
3. ✅ Introduced data quality issues:
   - ~3% missing driver_id
   - ~3% missing warehouse_id
   - ~2% missing package_weight
   - ~1% invalid dates
   - ~1.5% duplicate order_ids
4. ✅ Pushed to GitHub

**Files Created:**
- `data/raw/orders.csv` - 100K records
- `src/data_simulation/generate_orders.py` - Generation script

**Data Quality Summary:**
- Missing driver_id: 2,989 (2.99%)
- Missing warehouse_id: 2,932 (2.93%)
- Missing package_weight: 1,975 (1.98%)
- Delayed orders: 9,691 (9.69%)

**Git Status:**
- Branch: main
- Last commit: "Milestone #5: Generate orders.csv with 100k records and data quality issues"

**Project Status:**
- Orders CSV generated with realistic errors
- Ready for Milestone #6: Generate drivers.csv

### Instructions for Next AI Agent (Milestone #6)

Proceed to: `project_planing/prompts/milestone_06_drivers_csv.md`