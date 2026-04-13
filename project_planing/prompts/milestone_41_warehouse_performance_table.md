# Milestone #41: Create Warehouse Performance Table Schema

**Your Role:** Data Engineer

Create `database/migrations/013_create_warehouse_performance.sql`:
```sql
CREATE TABLE warehouse_performance (
    id SERIAL PRIMARY KEY,
    warehouse_id VARCHAR(10) REFERENCES warehouses(warehouse_id),
    date DATE NOT NULL,
    throughput INTEGER DEFAULT 0,
    avg_processing_time_minutes DECIMAL(10, 2),
    delays INTEGER DEFAULT 0,
    efficiency_score DECIMAL(5, 2)
);

CREATE INDEX idx_wh_perf_warehouse ON warehouse_performance(warehouse_id);
```

Run and commit.

### Milestone #41 Completed
- database/migrations/013_create_warehouse_performance.sql
- Next: Milestone #42