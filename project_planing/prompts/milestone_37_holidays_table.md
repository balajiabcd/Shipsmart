# Milestone #37: Create Holidays Table Schema

**Your Role:** Data Engineer

Create `database/migrations/009_create_holidays.sql`:
```sql
CREATE TABLE holidays (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(50) DEFAULT 'Germany',
    region VARCHAR(50),
    holiday_name VARCHAR(100) NOT NULL,
    holiday_type VARCHAR(20)
);

CREATE INDEX idx_holidays_date ON holidays(date);
```

Run and commit.