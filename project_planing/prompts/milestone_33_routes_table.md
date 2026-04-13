# Milestone #33: Create Routes Table Schema

**Your Role:** Data Engineer

Create `database/migrations/005_create_routes.sql`:
```sql
CREATE TABLE routes (
    route_id VARCHAR(20) PRIMARY KEY,
    origin_city VARCHAR(50),
    destination_city VARCHAR(50),
    distance_km DECIMAL(10, 2),
    avg_duration_minutes INTEGER,
    route_type VARCHAR(20),
    traffic_level VARCHAR(20)
);

CREATE INDEX idx_routes_cities ON routes(origin_city, destination_city);
```

Run and commit.

### Milestone #33 Completed
- database/migrations/005_create_routes.sql
- Next: Milestone #34