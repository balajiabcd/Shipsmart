-- Milestone #36: Traffic Table Migration

DROP TABLE IF EXISTS traffic CASCADE;

CREATE TABLE traffic (
    traffic_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    route_id VARCHAR(10) NOT NULL,
    hour INTEGER NOT NULL,
    congestion_level VARCHAR(20),
    avg_speed_kmh DECIMAL(6, 2),
    traffic_volume INTEGER,
    delay_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_hour CHECK (hour BETWEEN 0 AND 23),
    CONSTRAINT fk_traffic_route FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

CREATE INDEX idx_traffic_timestamp ON traffic(timestamp);
CREATE INDEX idx_traffic_route ON traffic(route_id);
CREATE INDEX idx_traffic_hour ON traffic(hour);

COMMENT ON TABLE traffic IS 'Traffic data for routes';