-- Milestone #32: Warehouses Table Migration

DROP TABLE IF EXISTS warehouses CASCADE;

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
    zone VARCHAR(5),
    region VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_warehouse_status CHECK (status IN ('active', 'expansion', 'closed')),
    CONSTRAINT chk_zone CHECK (zone IN ('A', 'B', 'C')),
    CONSTRAINT chk_region CHECK (region IN ('North', 'South', 'East', 'West', 'Central'))
);

CREATE INDEX idx_warehouses_city ON warehouses(city);
CREATE INDEX idx_warehouses_status ON warehouses(status);
CREATE INDEX idx_warehouses_region ON warehouses(region);

CREATE TRIGGER update_warehouses_timestamp
    BEFORE UPDATE ON warehouses
    FOR EACH ROW
    EXECUTE FUNCTION update_driver_timestamp();

COMMENT ON TABLE warehouses IS 'Warehouse locations and capacity';