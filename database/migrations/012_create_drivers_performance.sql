-- Milestone #40: Drivers Performance Table Migration

DROP TABLE IF EXISTS drivers_performance CASCADE;

CREATE TABLE drivers_performance (
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
    
    CONSTRAINT fk_perf_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    UNIQUE(driver_id, date)
);

CREATE INDEX idx_driver_perf_driver ON drivers_performance(driver_id);
CREATE INDEX idx_driver_perf_date ON drivers_performance(date);
CREATE INDEX idx_driver_perf_rating ON drivers_performance(rating);

COMMENT ON TABLE drivers_performance IS 'Driver daily performance metrics';