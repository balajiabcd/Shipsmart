# Milestone #29: Create Orders Table Schema

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #28 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Define Orders Table with Constraints

**Your Role:** Data Engineer

**Instructions:**
1. Create `database/migrations/001_create_orders.sql`:
   ```sql
   CREATE TABLE orders (
       order_id VARCHAR(20) PRIMARY KEY,
       customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
       driver_id VARCHAR(10) REFERENCES drivers(driver_id),
       warehouse_id VARCHAR(10) REFERENCES warehouses(warehouse_id),
       origin_lat DECIMAL(10, 7) NOT NULL,
       origin_lon DECIMAL(10, 7) NOT NULL,
       dest_lat DECIMAL(10, 7) NOT NULL,
       dest_lon DECIMAL(10, 7) NOT NULL,
       order_time TIMESTAMP NOT NULL,
       delivery_promise TIMESTAMP NOT NULL,
       actual_delivery TIMESTAMP,
       status VARCHAR(20) CHECK (status IN ('pending', 'in_transit', 'delivered', 'cancelled')),
       package_weight_kg DECIMAL(10, 2),
       package_type VARCHAR(20),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE INDEX idx_orders_customer ON orders(customer_id);
   CREATE INDEX idx_orders_driver ON orders(driver_id);
   CREATE INDEX idx_orders_status ON orders(status);
   CREATE INDEX idx_orders_order_time ON orders(order_time);
   ```

2. Run migration and verify
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*

### Milestone #29 Completed
- database/migrations/001_create_orders.sql
- Full constraints, triggers, indexes
- Next: Milestone #30