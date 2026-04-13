# Milestone #27: Design SQL Database Schema

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #26 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Create ERD and Define Database Tables

**Your Role:** Data Engineer

**Instructions:**
1. Create `docs/database_schema.md` with:
   - Entity-Relationship Diagram (text-based)
   - Table definitions with columns, types, constraints
   - Primary keys, foreign keys
   - Indexes

2. Key tables to design:
   - orders, drivers, vehicles, warehouses, routes
   - locations, weather, traffic, holidays
   - customers, delivery_events
   - drivers_performance, warehouse_performance

3. Example schema:
   ```sql
   CREATE TABLE orders (
       order_id VARCHAR(20) PRIMARY KEY,
       customer_id VARCHAR(20) REFERENCES customers(customer_id),
       driver_id VARCHAR(10) REFERENCES drivers(driver_id),
       warehouse_id VARCHAR(10) REFERENCES warehouses(warehouse_id),
       origin_lat DECIMAL(10, 7),
       origin_lon DECIMAL(10, 7),
       dest_lat DECIMAL(10, 7),
       dest_lon DECIMAL(10, 7),
       order_time TIMESTAMP,
       delivery_promise TIMESTAMP,
       actual_delivery TIMESTAMP,
       status VARCHAR(20),
       package_weight_kg DECIMAL(10, 2),
       package_type VARCHAR(20)
   );
   ```

4. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #27 Completed
- docs/database_schema.md
- ERD + 14 tables with constraints, foreign keys, indexes
- Next: Milestone #28