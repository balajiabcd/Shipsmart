# Milestone #34: Create Locations Table Schema

**Your Role:** Data Engineer

Create `database/migrations/006_create_locations.sql`:
```sql
CREATE TABLE locations (
    location_id VARCHAR(20) PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    region VARCHAR(50),
    population INTEGER
);

CREATE INDEX idx_locations_city ON locations(city);
```

Run and commit.

### Milestone #34 Completed
- database/migrations/006_create_locations.sql
- Next: Milestone #35