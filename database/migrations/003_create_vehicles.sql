-- Milestone #31: Vehicles Table Migration

DROP TABLE IF EXISTS vehicles CASCADE;

CREATE TABLE vehicles (
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
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    mileage INTEGER DEFAULT 0,
    fuel_type VARCHAR(20) DEFAULT 'diesel',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_vehicle_type CHECK (vehicle_type IN ('van', 'truck', 'motorcycle', 'scooter', 'car')),
    CONSTRAINT chk_vehicle_status CHECK (status IN ('active', 'maintenance', 'retired')),
    CONSTRAINT chk_vehicle_year CHECK (manufacturing_year BETWEEN 2000 AND 2030),
    CONSTRAINT chk_vehicle_capacity CHECK (capacity_kg > 0),
    CONSTRAINT chk_fuel_type CHECK (fuel_type IN ('diesel', 'petrol', 'electric', 'hybrid'))
);

CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_type ON vehicles(vehicle_type);
CREATE INDEX idx_vehicles_maintenance ON vehicles(maintenance_due);
CREATE INDEX idx_vehicles_plate ON vehicles(plate_number);

CREATE TRIGGER update_vehicles_timestamp
    BEFORE UPDATE ON vehicles
    FOR EACH ROW
    EXECUTE FUNCTION update_driver_timestamp();

COMMENT ON TABLE vehicles IS 'Vehicle fleet information';