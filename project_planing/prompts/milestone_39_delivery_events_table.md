# Milestone #39: Create Delivery Events Table Schema

**Your Role:** Data Engineer

Create `database/migrations/011_create_delivery_events.sql`:
```sql
CREATE TABLE delivery_events (
    event_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(20) REFERENCES orders(order_id),
    event_timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(30) CHECK (event_type IN ('created', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'failed')),
    location_id VARCHAR(20) REFERENCES locations(location_id)
);

CREATE INDEX idx_events_order ON delivery_events(order_id);
CREATE INDEX idx_events_timestamp ON delivery_events(event_timestamp);
```

Run and commit.

### Milestone #39 Completed
- database/migrations/011_create_delivery_events.sql
- Next: Milestone #40