-- Milestone #29: Orders Table Migration
-- This migration creates the orders table with full constraints

-- Drop table if exists for clean recreation
DROP TABLE IF EXISTS orders CASCADE;

-- Create orders table with constraints
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    driver_id VARCHAR(10),
    warehouse_id VARCHAR(10),
    origin_lat DECIMAL(10, 7) NOT NULL,
    origin_lon DECIMAL(10, 7) NOT NULL,
    dest_lat DECIMAL(10, 7) NOT NULL,
    dest_lon DECIMAL(10, 7) NOT NULL,
    order_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    scheduled_delivery_time TIMESTAMP NOT NULL,
    actual_delivery_time TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Check constraints
    CONSTRAINT chk_status CHECK (status IN ('pending', 'in_transit', 'delivered', 'cancelled')),
    CONSTRAINT chk_package_type CHECK (package_type IN ('document', 'parcel', 'fragile', 'oversized', 'electronics')),
    CONSTRAINT chk_shipping_type CHECK (shipping_type IN ('standard', 'express', 'overnight')),
    CONSTRAINT chk_priority CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    CONSTRAINT chk_delay_minutes CHECK (delay_minutes >= 0),
    CONSTRAINT chk_weight CHECK (package_weight_kg > 0),
    
    -- Foreign key constraints
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_orders_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    CONSTRAINT fk_orders_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- Create indexes for performance
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_driver ON orders(driver_id);
CREATE INDEX idx_orders_warehouse ON orders(warehouse_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_time ON orders(order_time);
CREATE INDEX idx_orders_scheduled ON orders(scheduled_delivery_time);
CREATE INDEX idx_orders_actual ON orders(actual_delivery_time);
CREATE INDEX idx_orders_priority ON orders(priority);
CREATE INDEX idx_orders_package_type ON orders(package_type);

-- Composite indexes for common queries
CREATE INDEX idx_orders_status_time ON orders(status, order_time);
CREATE INDEX idx_orders_driver_status ON orders(driver_id, status);
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- Add trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add trigger for delay calculation
CREATE OR REPLACE FUNCTION calculate_delay()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.actual_delivery_time IS NOT NULL AND NEW.scheduled_delivery_time IS NOT NULL THEN
        NEW.delay_minutes := EXTRACT(EPOCH FROM (NEW.actual_delivery_time - NEW.scheduled_delivery_time))/60;
        IF NEW.delay_minutes < 0 THEN
            NEW.delay_minutes := 0;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_order_delay
    BEFORE INSERT OR UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION calculate_delay();

-- Comments for documentation
COMMENT ON TABLE orders IS 'Main orders table storing all delivery orders';
COMMENT ON COLUMN orders.order_id IS 'Unique order identifier';
COMMENT ON COLUMN orders.customer_id IS 'Foreign key to customers';
COMMENT ON COLUMN orders.driver_id IS 'Foreign key to assigned driver';
COMMENT ON COLUMN orders.warehouse_id IS 'Foreign key to warehouse';
COMMENT ON COLUMN orders.status IS 'Order status: pending, in_transit, delivered, cancelled';
COMMENT ON COLUMN orders.delay_minutes IS 'Calculated delay in minutes from scheduled time';