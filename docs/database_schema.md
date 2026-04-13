# Shipsmart Database Schema

## Overview

This document defines the SQL database schema for the Shipsmart logistics system.

## Entity-Relationship Diagram

```
customers ---(customer_id)----> orders
                    |
                    v
                 orders ---(order_id)----> delivery_events
                                    ^
                                    |
drivers ----(driver_id)---------------+      |
              |                                     |
              v                                     v
vehicles ----(vehicle_id)                 locations
              |
              v
warehouses --(warehouse_id)-------------> routes
              |                              |
              +----------(warehouse_id)----->+
                           |
                           v
                     drivers_performance
                     warehouse_performance
                     vehicle_maintenance
```

## Core Tables

### customers

```sql
CREATE TABLE customers (
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
    account_status VARCHAR(20) DEFAULT 'active' CHECK (account_status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_status ON customers(account_status);
```

### drivers

```sql
CREATE TABLE drivers (
    driver_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    license_expiry DATE NOT NULL,
    vehicle_id VARCHAR(10) REFERENCES vehicles(vehicle_id),
    hire_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'on_leave', 'suspended')),
    rating DECIMAL(3, 2) DEFAULT 3.5 CHECK (rating BETWEEN 1 AND 5),
    total_deliveries INTEGER DEFAULT 0,
    on_time_rate DECIMAL(5, 4) DEFAULT 0.75,
    contact_phone VARCHAR(50),
    base_location VARCHAR(10) REFERENCES warehouses(warehouse_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_drivers_vehicle ON drivers(vehicle_id);
CREATE INDEX idx_drivers_base ON drivers(base_location);
```

### vehicles

```sql
CREATE TABLE vehicles (
    vehicle_id VARCHAR(10) PRIMARY KEY,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('van', 'truck', 'motorcycle', 'scooter', 'car')),
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    manufacturing_year INTEGER NOT NULL CHECK (manufacturing_year BETWEEN 2000 AND 2030),
    capacity_kg DECIMAL(10, 2) NOT NULL,
    plate_number VARCHAR(20) UNIQUE NOT NULL,
    vin VARCHAR(50) UNIQUE NOT NULL,
    insurance_expiry DATE NOT NULL,
    maintenance_due DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'maintenance', 'retired')),
    mileage INTEGER DEFAULT 0,
    fuel_type VARCHAR(20) DEFAULT 'diesel' CHECK (fuel_type IN ('diesel', 'petrol', 'electric', 'hybrid')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_type ON vehicles(vehicle_type);
CREATE INDEX idx_vehicles_maintenance ON vehicles(maintenance_due);
```

### warehouses

```sql
CREATE TABLE warehouses (
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
    zone VARCHAR(5) CHECK (zone IN ('A', 'B', 'C')),
    region VARCHAR(50) CHECK (region IN ('North', 'South', 'East', 'West', 'Central')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expansion', 'closed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_warehouses_city ON warehouses(city);
CREATE INDEX idx_warehouses_status ON warehouses(status);
CREATE INDEX idx_warehouses_region ON warehouses(region);
```

### orders

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
    scheduled_delivery_time TIMESTAMP NOT NULL,
    actual_delivery_time TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'in_transit', 'delivered', 'cancelled')),
    delay_minutes INTEGER,
    package_weight_kg DECIMAL(10, 2),
    package_dimensions_length_cm INTEGER,
    package_dimensions_width_cm INTEGER,
    package_dimensions_height_cm INTEGER,
    package_type VARCHAR(20) CHECK (package_type IN ('document', 'parcel', 'fragile', 'oversized', 'electronics')),
    shipping_type VARCHAR(20) DEFAULT 'standard' CHECK (shipping_type IN ('standard', 'express', 'overnight')),
    priority VARCHAR(20) DEFAULT 'low' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    estimated_cost_eur DECIMAL(10, 2),
    actual_cost_eur DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_driver ON orders(driver_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_time ON orders(order_time);
CREATE INDEX idx_orders_delivery_time ON orders(actual_delivery_time);
CREATE INDEX idx_orders_status_time ON orders(status, order_time);
```

### locations

```sql
CREATE TABLE locations (
    location_id VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    region VARCHAR(50),
    population INTEGER,
    location_type VARCHAR(20) CHECK (location_type IN ('residential', 'commercial', 'industrial')),
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_city ON locations(city);
CREATE INDEX idx_locations_region ON locations(region);
```

### routes

```sql
CREATE TABLE routes (
    route_id VARCHAR(10) PRIMARY KEY,
    origin_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    avg_duration_minutes INTEGER,
    route_type VARCHAR(20) CHECK (route_type IN ('highway', 'secondary', 'local', 'mixed', 'urban')),
    traffic_level VARCHAR(20),
    toll_roads BOOLEAN DEFAULT FALSE,
    preferred_times VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_routes_origin ON routes(origin_city);
CREATE INDEX idx_routes_destination ON routes(destination_city);
```

### weather

```sql
CREATE TABLE weather (
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

CREATE INDEX idx_weather_timestamp ON weather(timestamp);
CREATE INDEX idx_weather_location ON weather(location_city);
```

### traffic

```sql
CREATE TABLE traffic (
    traffic_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    route_id VARCHAR(10) NOT NULL REFERENCES routes(route_id),
    hour INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    congestion_level VARCHAR(20),
    avg_speed_kmh DECIMAL(6, 2),
    traffic_volume INTEGER,
    delay_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_traffic_route ON traffic(route_id);
CREATE INDEX idx_traffic_timestamp ON traffic(timestamp);
```

### holidays

```sql
CREATE TABLE holidays (
    holiday_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(50) DEFAULT 'Germany',
    region VARCHAR(50),
    holiday_name VARCHAR(200) NOT NULL,
    holiday_type VARCHAR(20) CHECK (holiday_type IN ('national', 'regional', 'movable', 'observance')),
    celebrations_expected INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_holidays_date ON holidays(date);
CREATE INDEX idx_holidays_region ON holidays(region);
```

### delivery_events

```sql
CREATE TABLE delivery_events (
    event_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL REFERENCES orders(order_id),
    timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(30) NOT NULL CHECK (event_type IN ('created', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'failed_attempt')),
    location_id VARCHAR(10) REFERENCES locations(location_id),
    driver_id VARCHAR(10) REFERENCES drivers(driver_id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_delivery_events_order ON delivery_events(order_id);
CREATE INDEX idx_delivery_events_timestamp ON delivery_events(timestamp);
CREATE INDEX idx_delivery_events_driver ON delivery_events(driver_id);
```

### drivers_performance

```sql
CREATE TABLE drivers_performance (
    performance_id SERIAL PRIMARY KEY,
    driver_id VARCHAR(10) NOT NULL REFERENCES drivers(driver_id),
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

CREATE INDEX idx_driver_perf_driver ON drivers_performance(driver_id);
CREATE INDEX idx_driver_perf_date ON drivers_performance(date);
```

### warehouse_performance

```sql
CREATE TABLE warehouse_performance (
    performance_id SERIAL PRIMARY KEY,
    warehouse_id VARCHAR(10) NOT NULL REFERENCES warehouses(warehouse_id),
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

CREATE INDEX idx_warehouse_perf_warehouse ON warehouse_performance(warehouse_id);
CREATE INDEX idx_warehouse_perf_date ON warehouse_performance(date);
```

## Views

### v_order_summary

```sql
CREATE VIEW v_order_summary AS
SELECT 
    o.order_id,
    c.customer_id,
    c.full_name AS customer_name,
    d.full_name AS driver_name,
    w.warehouse_name,
    o.order_time,
    o.scheduled_delivery_time,
    o.actual_delivery_time,
    o.status,
    o.delay_minutes,
    o.package_type,
    o.shipping_type,
    o.priority
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN drivers d ON o.driver_id = d.driver_id
LEFT JOIN warehouses w ON o.warehouse_id = w.warehouse_id;
```

### v_driver_stats

```sql
CREATE VIEW v_driver_stats AS
SELECT 
    dp.driver_id,
    d.full_name,
    d.status,
    COUNT(*) AS total_days,
    SUM(dp.total_deliveries) AS total_deliveries,
    SUM(dp.on_time_deliveries) AS total_on_time,
    AVG(dp.rating) AS avg_rating,
    AVG(dp.on_time_rate) AS avg_on_time_rate
FROM drivers_performance dp
JOIN drivers d ON dp.driver_id = d.driver_id
GROUP BY dp.driver_id, d.full_name, d.status;
```

## Summary

- **Total Tables**: 14
- **Total Views**: 2
- **Indexes**: 30+
- **Foreign Keys**: Established for all relationships
- **Data Integrity**: CHECK constraints, NOT NULL, UNIQUE