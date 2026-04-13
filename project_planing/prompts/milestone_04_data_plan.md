# Milestone #4: Design Data Simulation Plan

---

## Section 1: Instructions from Previous AI Agent

**From Milestone #3:**
- pyproject.toml created
- Makefile created
- scripts/setup.bat and setup.sh created

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Design Data Simulation Plan - Define Schemas for 15-20 CSV Files

**Project Context:**
- Project: Shipsmart
- **GitHub Repository:** https://github.com/balajiabcd/Shipsmart

**Your Role:**
You are a **Data Engineer** designing the data simulation plan.

**Instructions:**

1. **Create Data Simulation Plan Document**
   Create `docs/data_simulation_plan.md` with:

   **CSV Files to Generate (20 files):**
   
   | # | File Name | Records | Key Fields | Data Quality Issues |
   |---|-----------|---------|-------------|---------------------|
   | 1 | orders.csv | 100,000 | order_id, customer_id, driver_id, warehouse_id, origin, destination, order_time, delivery_time, status | 3% missing values |
   | 2 | drivers.csv | 500 | driver_id, name, license_number, vehicle_id, hire_date, status | Inconsistent date formats |
   | 3 | vehicles.csv | 300 | vehicle_id, type, capacity, plate_number, maintenance_due | 2% outliers in capacity |
   | 4 | warehouses.csv | 20 | warehouse_id, location, capacity, manager | 5% missing fields |
   | 5 | routes.csv | 1,000 | route_id, origin, destination, distance, avg_duration | Duplicate entries |
   | 6 | locations.csv | 500 | location_id, city, lat, long, region | Geocoding issues |
   | 7 | weather.csv | 50,000 | date, location_id, temperature, condition, humidity | 10% null values |
   | 8 | traffic.csv | 50,000 | date, route_id, congestion_level, avg_speed | Inconsistent data |
   | 9 | holidays.csv | 500 | date, country, region, holiday_name | Format issues |
   | 10 | customers.csv | 20,000 | customer_id, name, email, phone, address | PII data (anonymize) |
   | 11 | delivery_events.csv | 200,000 | event_id, order_id, timestamp, event_type, location | Missing timestamps |
   | 12 | drivers_performance.csv | 50,000 | driver_id, date, deliveries, on_time, late, rating | Historical data |
   | 13 | warehouse_performance.csv | 5,000 | warehouse_id, date, throughput, delays, efficiency | Missing metrics |
   | 14 | route_traffic_history.csv | 100,000 | route_id, date, time, traffic_level | Inconsistent levels |
   | 15 | vehicle_maintenance.csv | 5,000 | vehicle_id, date, maintenance_type, cost, next_due | Random gaps |
   | 16 | fuel_prices.csv | 10,000 | date, location, fuel_type, price | Outliers |
   | 17 | customer_feedback.csv | 30,000 | order_id, customer_id, rating, comment, timestamp | Missing comments |
   | 18 | competitor_data.csv | 1,000 | competitor_id, region, market_share, pricing | Limited data |
   | 19 | delay_reasons.csv | 10,000 | delay_id, order_id, reason, severity, duration | Categorical issues |
   | 20 | demand_forecasting.csv | 20,000 | date, region, predicted_demand, actual_demand | Forecast errors |

2. **Define Data Quality Issues to Introduce**
   - Missing values: 3-10% per file
   - Outliers: 2-5% numeric fields
   - Inconsistencies: Date formats, categorical values
   - Duplicates: 1-3% of records
   - PII issues: Customer data needs anonymization

3. **Create Schema Definitions**
   For each file, define:
   - Column names and types
   - Value ranges
   - Constraints

4. **Commit and Push**
   ```bash
   git add docs/data_simulation_plan.md
   git commit -m "Add data simulation plan with 20 CSV schemas"
   git push
   ```

**Subagent Task:**
If needed, ask Team Lead for approval on file count and scope.

---

## Section 3: Instructions for Next AI Agent

### Milestone Completion Summary

**Completed Tasks:**
1. ✅ Created comprehensive data simulation plan document
2. ✅ Defined schemas for 20 CSV files with full column definitions
3. ✅ Documented data quality issues to introduce
4. ✅ Pushed to GitHub

**Files Created:**
- `docs/data_simulation_plan.md` - Complete data simulation plan

**Data Files Defined (20):**
1. orders.csv (100K records)
2. drivers.csv (500)
3. vehicles.csv (300)
4. warehouses.csv (20)
5. routes.csv (1K)
6. locations.csv (500)
7. weather.csv (50K)
8. traffic.csv (50K)
9. holidays.csv (500)
10. customers.csv (20K)
11. delivery_events.csv (200K)
12. drivers_performance.csv (50K)
13. warehouse_performance.csv (5K)
14. route_traffic_history.csv (100K)
15. vehicle_maintenance.csv (5K)
16. fuel_prices.csv (10K)
17. customer_feedback.csv (30K)
18. competitor_data.csv (1K)
19. delay_reasons.csv (10K)
20. demand_forecasting.csv (20K)

**Git Status:**
- Branch: main
- Last commit: "Milestone #4: Add data simulation plan with 20 CSV schemas"

**Project Status:**
- Data simulation plan complete
- Ready for Milestone #5: Generate orders.csv

### Instructions for Next AI Agent (Milestone #5)

Proceed to: `project_planing/prompts/milestone_05_orders_csv.md`