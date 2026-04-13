# Milestone #55: Create Database Views

**Your Role:** Data Engineer

Create `database/views.sql`:
```sql
-- Orders with customer and driver details
CREATE VIEW v_orders_details AS
SELECT o.*, c.name as customer_name, d.name as driver_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN drivers d ON o.driver_id = d.driver_id;

-- Delayed orders
CREATE VIEW v_delayed_orders AS
SELECT * FROM orders 
WHERE status = 'delivered' 
AND actual_delivery > delivery_promise;

-- Daily performance summary
CREATE VIEW v_daily_performance AS
SELECT date, 
       SUM(total_deliveries) as total_deliveries,
       SUM(on_time_count) as on_time,
       AVG(rating) as avg_rating
FROM drivers_performance
GROUP BY date;
```

Run views and commit.