-- Shipsmart Database Schema Initialization
-- Run this script to create all tables

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    street_address VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    customer_since DATE NOT NULL,
    customer_type VARCHAR(20) CHECK (customer_type IN ('individual', 'business')),
    credit_limit DECIMAL(10, 2) DEFAULT 1000,
    preferred_shipping VARCHAR(20) DEFAULT 'standard',
    account_status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drivers table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    license_expiry DATE NOT NULL,
    vehicle_id VARCHAR(10),
    hire_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    rating DECIMAL(3, 2) DEFAULT 3.5,
    total_deliveries INTEGER DEFAULT 0,
    on_time_rate DECIMAL(5, 4) DEFAULT 0.75,
    contact_phone VARCHAR(50),
    base_location VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id VARCHAR(10) PRIMARY KEY,
    vehicle_type VARCHAR(20) NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    manufacturing_year INTEGER NOT NULL,
    capacity_kg DECIMAL(10, 2) NOT NULL,
    plate_number VARCHAR(20) UNIQUE NOT NULL,
    vin VARCHAR(50) UNIQUE NOT NULL,
    insurance_expiry DATE NOT NULL,
    maintenance_due DATE,
    status VARCHAR(20) DEFAULT 'active',
    mileage INTEGER DEFAULT 0,
    fuel_type VARCHAR(20) DEFAULT 'diesel',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Warehouses table
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id VARCHAR(10) PRIMARY KEY,
    warehouse_name VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    capacity_sqm INTEGER NOT NULL,
    manager_name VARCHAR(200),
    manager_contact VARCHAR(50),
    email VARCHAR(255),
    established_date DATE NOT NULL,
    operating_hours VARCHAR(50) DEFAULT '06:00-22:00',
    zone VARCHAR(5),
    region VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    driver_id VARCHAR(10),
    warehouse_id VARCHAR(10),
    origin_lat DECIMAL(10, 7) NOT NULL,
    origin_lon DECIMAL(10, 7) NOT NULL,
    dest_lat DECIMAL(10, 7) NOT NULL,
    dest_lon DECIMAL(10, 7) NOT NULL,
    order_time TIMESTAMP NOT NULL,
    scheduled_delivery_time TIMESTAMP NOT NULL,
    actual_delivery_time TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    delay_minutes INTEGER,
    package_weight_kg DECIMAL(10, 2),
    package_dimensions_length_cm INTEGER,
    package_dimensions_width_cm INTEGER,
    package_dimensions_height_cm INTEGER,
    package_type VARCHAR(20),
    shipping_type VARCHAR(20) DEFAULT 'standard',
    priority VARCHAR(20) DEFAULT 'low',
    estimated_cost_eur DECIMAL(10, 2),
    actual_cost_eur DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Locations table
CREATE TABLE IF NOT EXISTS locations (
    location_id VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    region VARCHAR(50),
    population INTEGER,
    location_type VARCHAR(20),
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Routes table
CREATE TABLE IF NOT EXISTS routes (
    route_id VARCHAR(10) PRIMARY KEY,
    origin_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    avg_duration_minutes INTEGER,
    route_type VARCHAR(20),
    traffic_level VARCHAR(20),
    toll_roads BOOLEAN DEFAULT FALSE,
    preferred_times VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather table
CREATE TABLE IF NOT EXISTS weather (
    weather_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    location_city VARCHAR(100) NOT NULL,
    temperature_celsius DECIMAL(5, 1),
    humidity_percent DECIMAL(5, 2),
    wind_speed_kmh DECIMAL(6, 2),
    wind_direction VARCHAR(5),
    condition VARCHAR(20),
    visibility_km DECIMAL(6, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Traffic table
CREATE TABLE IF NOT EXISTS traffic (
    traffic_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    route_id VARCHAR(10) NOT NULL,
    hour INTEGER NOT NULL,
    congestion_level VARCHAR(20),
    avg_speed_kmh DECIMAL(6, 2),
    traffic_volume INTEGER,
    delay_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Holidays table
CREATE TABLE IF NOT EXISTS holidays (
    holiday_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(50) DEFAULT 'Germany',
    region VARCHAR(50),
    holiday_name VARCHAR(200) NOT NULL,
    holiday_type VARCHAR(20),
    celebrations_expected INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Delivery events table
CREATE TABLE IF NOT EXISTS delivery_events (
    event_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    location_id VARCHAR(10),
    driver_id VARCHAR(10),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drivers performance table
CREATE TABLE IF NOT EXISTS drivers_performance (
    performance_id SERIAL PRIMARY KEY,
    driver_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    total_deliveries INTEGER NOT NULL,
    on_time_deliveries INTEGER NOT NULL,
    late_deliveries INTEGER NOT NULL,
    rating DECIMAL(3, 2),
    customer_complaints INTEGER DEFAULT 0,
    fuel_efficiency DECIMAL(6, 2),
    accidents INTEGER DEFAULT 0,
    overtime_hours DECIMAL(5, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(driver_id, date)
);

-- Warehouse performance table
CREATE TABLE IF NOT EXISTS warehouse_performance (
    performance_id SERIAL PRIMARY KEY,
    warehouse_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    inbound_volume INTEGER NOT NULL,
    outbound_volume INTEGER NOT NULL,
    throughput INTEGER NOT NULL,
    avg_processing_time_minutes DECIMAL(6, 2),
    delays_count INTEGER DEFAULT 0,
    efficiency_score DECIMAL(5, 2),
    staff_count INTEGER NOT NULL,
    overtime_hours DECIMAL(6, 1),
    error_rate DECIMAL(5, 2),
    returns_received INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(warehouse_id, date)
);

-- Create foreign key constraints
ALTER TABLE drivers ADD CONSTRAINT fk_drivers_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id);
ALTER TABLE drivers ADD CONSTRAINT fk_drivers_base FOREIGN KEY (base_location) REFERENCES warehouses(warehouse_id);
ALTER TABLE orders ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
ALTER TABLE orders ADD CONSTRAINT fk_orders_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id);
ALTER TABLE orders ADD CONSTRAINT fk_orders_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id);
ALTER TABLE delivery_events ADD CONSTRAINT fk_events_order FOREIGN KEY (order_id) REFERENCES orders(order_id);
ALTER TABLE delivery_events ADD CONSTRAINT fk_events_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id);
ALTER TABLE drivers_performance ADD CONSTRAINT fk_perf_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id);
ALTER TABLE warehouse_performance ADD CONSTRAINT fk_perf_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id);
ALTER TABLE traffic ADD CONSTRAINT fk_traffic_route FOREIGN KEY (route_id) REFERENCES routes(route_id);

-- Create indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_driver ON orders(driver_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_time ON orders(order_time);
CREATE INDEX idx_weather_timestamp ON weather(timestamp);
CREATE INDEX idx_traffic_route ON traffic(route_id);
CREATE INDEX idx_delivery_events_order ON delivery_events(order_id);
CREATE INDEX idx_driver_perf_driver ON drivers_performance(driver_id);
CREATE INDEX idx_driver_perf_date ON drivers_performance(date);
CREATE INDEX idx_warehouse_perf_warehouse ON warehouse_performance(warehouse_id);
CREATE INDEX idx_warehouse_perf_date ON warehouse_performance(date);

-- Create views
CREATE OR REPLACE VIEW v_order_summary AS
SELECT 
    o.order_id, o.customer_id, c.full_name AS customer_name,
    d.full_name AS driver_name, w.warehouse_name,
    o.order_time, o.scheduled_delivery_time, o.actual_delivery_time,
    o.status, o.delay_minutes, o.package_type, o.shipping_type, o.priority
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN drivers d ON o.driver_id = d.driver_id
LEFT JOIN warehouses w ON o.warehouse_id = w.warehouse_id;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO shipsmart;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO shipsmart;