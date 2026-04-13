# Milestone #35: Create Weather Table Schema

**Your Role:** Data Engineer

Create `database/migrations/007_create_weather.sql`:
```sql
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    location_id VARCHAR(20) REFERENCES locations(location_id),
    temperature DECIMAL(5, 2),
    condition VARCHAR(20),
    humidity DECIMAL(5, 2),
    wind_speed DECIMAL(5, 2)
);

CREATE INDEX idx_weather_date ON weather(date);
CREATE INDEX idx_weather_location ON weather(location_id);
```

Run and commit.

### Milestone #35 Completed
- database/migrations/007_create_weather.sql
- All milestones 26-35 COMPLETE