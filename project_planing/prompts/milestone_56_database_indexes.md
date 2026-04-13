# Milestone #56: Create Database Indexes

**Your Role:** Data Engineer

Create `database/indexes.sql`:
```sql
-- Performance indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_driver_id ON orders(driver_id);
CREATE INDEX idx_orders_warehouse_id ON orders(warehouse_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_time ON orders(order_time);

CREATE INDEX idx_delivery_events_order_id ON delivery_events(order_id);
CREATE INDEX idx_delivery_events_timestamp ON delivery_events(event_timestamp);

CREATE INDEX idx_drivers_perf_driver_date ON drivers_performance(driver_id, date);
CREATE INDEX idx_warehouse_perf_date ON warehouse_performance(date);

-- Composite indexes for common queries
CREATE INDEX idx_orders_status_time ON orders(status, order_time);
CREATE INDEX idx_delivery_events_type ON delivery_events(event_type);
```

Run indexes and analyze query performance. Commit.