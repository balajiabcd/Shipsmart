# Milestone #31: Create Vehicles Table Schema

**Your Role:** Data Engineer

Create `database/migrations/003_create_vehicles.sql`:
```sql
CREATE TABLE vehicles (
    vehicle_id VARCHAR(20) PRIMARY KEY,
    vehicle_type VARCHAR(20) CHECK (vehicle_type IN ('van', 'truck', 'motorcycle')),
    capacity_kg DECIMAL(10, 2),
    plate_number VARCHAR(20) UNIQUE NOT NULL,
    manufacturing_year INTEGER,
    maintenance_due DATE,
    insurance_expiry DATE,
    status VARCHAR(20) CHECK (status IN ('active', 'maintenance', 'retired'))
);

CREATE INDEX idx_vehicles_status ON vehicles(status);
```

Run and commit.

### Milestone #31 Completed
- database/migrations/003_create_vehicles.sql
- Next: Milestone #32