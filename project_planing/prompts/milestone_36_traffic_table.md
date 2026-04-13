# Milestone #36: Create Traffic Table Schema

**Your Role:** Data Engineer

Create `database/migrations/008_create_traffic.sql`:
```sql
CREATE TABLE traffic (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    route_id VARCHAR(20) REFERENCES routes(route_id),
    hour INTEGER CHECK (hour >= 0 AND hour <= 23),
    congestion_level INTEGER CHECK (congestion_level >= 1 AND congestion_level <= 10),
    avg_speed DECIMAL(6, 2)
);

CREATE INDEX idx_traffic_date ON traffic(date);
CREATE INDEX idx_traffic_route ON traffic(route_id);
```

Run and commit.