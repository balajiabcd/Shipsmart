-- Milestone #37: Holidays Table Migration

DROP TABLE IF EXISTS holidays CASCADE;

CREATE TABLE holidays (
    holiday_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(50) DEFAULT 'Germany',
    region VARCHAR(50),
    holiday_name VARCHAR(200) NOT NULL,
    holiday_type VARCHAR(20),
    celebrations_expected INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_holiday_type CHECK (holiday_type IN ('national', 'regional', 'movable', 'observance'))
);

CREATE INDEX idx_holidays_date ON holidays(date);
CREATE INDEX idx_holidays_region ON holidays(region);

COMMENT ON TABLE holidays IS 'Public holidays data';