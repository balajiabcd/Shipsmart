# Milestone #38: Create Customers Table Schema

**Your Role:** Data Engineer

Create `database/migrations/010_create_customers.sql`:
```sql
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    registration_date DATE
);

CREATE INDEX idx_customers_email ON customers(email);
```

Run and commit.