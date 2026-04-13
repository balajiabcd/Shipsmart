-- Milestone #41: Warehouse Performance Table Migration

DROP TABLE IF EXISTS warehouse_performance CASCADE;

CREATE TABLE warehouse_performance (
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
    
    CONSTRAINT fk_wh_perf_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    UNIQUE(warehouse_id, date)
);

CREATE INDEX idx_wh_perf_warehouse ON warehouse_performance(warehouse_id);
CREATE INDEX idx_wh_perf_date ON warehouse_performance(date);
CREATE INDEX idx_wh_perf_efficiency ON warehouse_performance(efficiency_score);

COMMENT ON TABLE warehouse_performance IS 'Warehouse daily performance metrics';