# Milestone #30: Create Drivers Table Schema

**Your Role:** Data Engineer

Create `database/migrations/002_create_drivers.sql`:
```sql
CREATE TABLE drivers (
    driver_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    vehicle_id VARCHAR(20) REFERENCES vehicles(vehicle_id),
    hire_date DATE,
    license_expiry DATE,
    status VARCHAR(20) CHECK (status IN ('active', 'on_leave', 'suspended')),
    rating DECIMAL(3,2) CHECK (rating >= 1 AND rating <= 5),
    total_deliveries INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drivers_status ON drivers(status);
```

Run and commit.

### Milestone #30 Completed
- database/migrations/002_create_drivers.sql
- Full constraints and triggers
- Next: Milestone #31