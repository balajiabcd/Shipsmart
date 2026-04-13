-- Milestone #33: Routes Table Migration

DROP TABLE IF EXISTS routes CASCADE;

CREATE TABLE routes (
    route_id VARCHAR(10) PRIMARY KEY,
    origin_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    avg_duration_minutes INTEGER,
    route_type VARCHAR(20),
    traffic_level VARCHAR(20),
    toll_roads BOOLEAN DEFAULT FALSE,
    preferred_times VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_route_type CHECK (route_type IN ('highway', 'secondary', 'local', 'mixed', 'urban'))
);

CREATE INDEX idx_routes_origin ON routes(origin_city);
CREATE INDEX idx_routes_destination ON routes(destination_city);
CREATE INDEX idx_routes_cities ON routes(origin_city, destination_city);

COMMENT ON TABLE routes IS 'Delivery route information';