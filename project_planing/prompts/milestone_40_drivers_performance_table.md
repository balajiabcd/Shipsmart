# Milestone #40: Create Drivers Performance Table Schema

**Your Role:** Data Engineer

Create `database/migrations/012_create_drivers_performance.sql`:
```sql
CREATE TABLE drivers_performance (
    id SERIAL PRIMARY KEY,
    driver_id VARCHAR(10) REFERENCES drivers(driver_id),
    date DATE NOT NULL,
    total_deliveries INTEGER DEFAULT 0,
    on_time_count INTEGER DEFAULT 0,
    late_count INTEGER DEFAULT 0,
    rating DECIMAL(3, 2)
);

CREATE INDEX idx_driver_perf_driver ON drivers_performance(driver_id);
CREATE INDEX idx_driver_perf_date ON drivers_performance(date);
```

Run and commit.