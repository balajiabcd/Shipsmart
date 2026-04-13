-- Database Indexes for Shipsmart

-- Orders table indexes
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_driver_id ON orders(driver_id);
CREATE INDEX IF NOT EXISTS idx_orders_warehouse_id ON orders(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_order_time ON orders(order_time);
CREATE INDEX IF NOT EXISTS idx_orders_scheduled_delivery ON orders(scheduled_delivery_time);

-- Composite index for status and time queries
CREATE INDEX IF NOT EXISTS idx_orders_status_time ON orders(status, order_time);

-- Delivery events indexes
CREATE INDEX IF NOT EXISTS idx_delivery_events_order_id ON delivery_events(order_id);
CREATE INDEX IF NOT EXISTS idx_delivery_events_timestamp ON delivery_events(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_delivery_events_type ON delivery_events(event_type);
CREATE INDEX IF NOT EXISTS idx_delivery_events_driver_id ON delivery_events(driver_id);

-- Drivers performance indexes
CREATE INDEX IF NOT EXISTS idx_drivers_perf_driver_date ON drivers_performance(driver_id, date);

-- Warehouse performance indexes
CREATE INDEX IF NOT EXISTS idx_warehouse_perf_date ON warehouse_performance(date);
CREATE INDEX IF NOT EXISTS idx_warehouse_perf_warehouse_date ON warehouse_performance(warehouse_id, date);

-- Customers indexes
CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_city ON customers(city);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(account_status);

-- Drivers indexes
CREATE INDEX IF NOT EXISTS idx_drivers_driver_id ON drivers(driver_id);
CREATE INDEX IF NOT EXISTS idx_drivers_status ON drivers(status);
CREATE INDEX IF NOT EXISTS idx_drivers_base_location ON drivers(base_location);

-- Vehicles indexes
CREATE INDEX IF NOT EXISTS idx_vehicles_vehicle_id ON vehicles(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status);
CREATE INDEX IF NOT EXISTS idx_vehicles_type ON vehicles(vehicle_type);

-- Locations indexes
CREATE INDEX IF NOT EXISTS idx_locations_city ON locations(city);
CREATE INDEX IF NOT EXISTS idx_locations_region ON locations(region);

-- Routes indexes
CREATE INDEX IF NOT EXISTS idx_routes_route_id ON routes(route_id);
CREATE INDEX IF NOT EXISTS idx_routes_origin_dest ON routes(origin_city, destination_city);

-- Weather indexes
CREATE INDEX IF NOT EXISTS idx_weather_timestamp ON weather(timestamp);
CREATE INDEX IF NOT EXISTS idx_weather_location ON weather(location_city);

-- Traffic indexes
CREATE INDEX IF NOT EXISTS idx_traffic_timestamp ON traffic(timestamp);
CREATE INDEX IF NOT EXISTS idx_traffic_route ON traffic(route_id);

-- Holidays indexes
CREATE INDEX IF NOT EXISTS idx_holidays_date ON holidays(date);
CREATE INDEX IF NOT EXISTS idx_holidays_region ON holidays(region);

-- Warehouses indexes
CREATE INDEX IF NOT EXISTS idx_warehouses_warehouse_id ON warehouses(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_warehouses_city ON warehouses(city);
CREATE INDEX IF NOT EXISTS idx_warehouses_status ON warehouses(status);