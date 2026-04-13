-- Database Views for Shipsmart

-- Orders with customer and driver details
CREATE OR REPLACE VIEW v_orders_details AS
SELECT 
    o.order_id,
    o.order_time,
    o.scheduled_delivery_time,
    o.actual_delivery_time,
    o.status,
    o.package_weight_kg,
    o.delivery_address,
    o.customer_id,
    o.driver_id,
    o.warehouse_id,
    o.delay_minutes,
    c.first_name AS customer_first_name,
    c.last_name AS customer_last_name,
    c.city AS customer_city,
    d.full_name AS driver_name,
    d.rating AS driver_rating
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN drivers d ON o.driver_id = d.driver_id;

-- Delayed orders view
CREATE OR REPLACE VIEW v_delayed_orders AS
SELECT 
    order_id,
    order_time,
    scheduled_delivery_time,
    actual_delivery_time,
    delay_minutes,
    customer_id,
    driver_id
FROM orders 
WHERE status = 'delivered' 
AND delay_minutes > 0;

-- Daily performance summary for drivers
CREATE OR REPLACE VIEW v_daily_driver_performance AS
SELECT 
    date,
    driver_id,
    SUM(total_deliveries) AS total_deliveries,
    SUM(on_time_deliveries) AS on_time_deliveries,
    SUM(late_deliveries) AS late_deliveries,
    AVG(rating) AS avg_rating,
    SUM(customer_complaints) AS total_complaints,
    SUM(accidents) AS total_accidents
FROM drivers_performance
GROUP BY date, driver_id;

-- Daily warehouse performance summary
CREATE OR REPLACE VIEW v_daily_warehouse_performance AS
SELECT 
    date,
    warehouse_id,
    SUM(inbound_volume) AS total_inbound,
    SUM(outbound_volume) AS total_outbound,
    AVG(efficiency_score) AS avg_efficiency,
    SUM(delays_count) AS total_delays,
    AVG(error_rate) AS avg_error_rate
FROM warehouse_performance
GROUP BY date, warehouse_id;

-- Delivery events timeline for orders
CREATE OR REPLACE VIEW v_delivery_timeline AS
SELECT 
    order_id,
    MIN(timestamp) AS first_event,
    MAX(timestamp) AS last_event,
    COUNT(*) AS event_count,
    STRING_AGG(DISTINCT event_type, ', ' ORDER BY timestamp) AS event_types
FROM delivery_events
GROUP BY order_id;

-- Customer order summary
CREATE OR REPLACE VIEW v_customer_order_summary AS
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN o.delay_minutes > 0 THEN 1 ELSE 0 END) AS delayed_orders,
    AVG(o.delay_minutes) AS avg_delay_minutes
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city;