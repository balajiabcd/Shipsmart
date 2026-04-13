-- Milestone #30: Drivers Table Migration

DROP TABLE IF EXISTS drivers CASCADE;

CREATE TABLE drivers (
    driver_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    license_expiry DATE NOT NULL,
    vehicle_id VARCHAR(10),
    hire_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    rating DECIMAL(3, 2) DEFAULT 3.5,
    total_deliveries INTEGER DEFAULT 0,
    on_time_rate DECIMAL(5, 4) DEFAULT 0.75,
    contact_phone VARCHAR(50),
    base_location VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_driver_status CHECK (status IN ('active', 'on_leave', 'suspended')),
    CONSTRAINT chk_driver_rating CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT chk_driver_deliveries CHECK (total_deliveries >= 0),
    CONSTRAINT chk_on_time_rate CHECK (on_time_rate >= 0 AND on_time_rate <= 1),
    
    CONSTRAINT fk_drivers_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    CONSTRAINT fk_drivers_base FOREIGN KEY (base_location) REFERENCES warehouses(warehouse_id)
);

CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_drivers_vehicle ON drivers(vehicle_id);
CREATE INDEX idx_drivers_base ON drivers(base_location);
CREATE INDEX idx_drivers_rating ON drivers(rating);
CREATE INDEX idx_drivers_hire_date ON drivers(hire_date);

CREATE OR REPLACE FUNCTION update_driver_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_drivers_timestamp
    BEFORE UPDATE ON drivers
    FOR EACH ROW
    EXECUTE FUNCTION update_driver_timestamp();

COMMENT ON TABLE drivers IS 'Driver information table';
COMMENT ON COLUMN drivers.driver_id IS 'Unique driver ID';
COMMENT ON COLUMN drivers.full_name IS 'Driver full name';
COMMENT ON COLUMN drivers.license_number IS 'Driving license number';
COMMENT ON COLUMN drivers.rating IS 'Performance rating 1-5';