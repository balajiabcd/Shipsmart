-- Milestone #34: Locations Table Migration

DROP TABLE IF EXISTS locations CASCADE;

CREATE TABLE locations (
    location_id VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    region VARCHAR(50),
    population INTEGER,
    location_type VARCHAR(20),
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_location_type CHECK (location_type IN ('residential', 'commercial', 'industrial'))
);

CREATE INDEX idx_locations_city ON locations(city);
CREATE INDEX idx_locations_region ON locations(region);
CREATE INDEX idx_locations_postal ON locations(postal_code);

COMMENT ON TABLE locations IS 'Geographic locations for deliveries';