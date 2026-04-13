# Milestone #32: Create Warehouses Table Schema

**Your Role:** Data Engineer

Create `database/migrations/004_create_warehouses.sql`:
```sql
CREATE TABLE warehouses (
    warehouse_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    capacity INTEGER,
    manager_name VARCHAR(100),
    contact_phone VARCHAR(20),
    email VARCHAR(100),
    established_date DATE,
    operating_hours VARCHAR(50)
);
```

Run and commit.

### Milestone #32 Completed
- database/migrations/004_create_warehouses.sql
- Next: Milestone #33