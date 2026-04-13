-- Milestone #38: Customers Table Migration

DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    street_address VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    customer_since DATE NOT NULL,
    customer_type VARCHAR(20) DEFAULT 'individual',
    credit_limit DECIMAL(10, 2) DEFAULT 1000,
    preferred_shipping VARCHAR(20) DEFAULT 'standard',
    account_status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_customer_type CHECK (customer_type IN ('individual', 'business')),
    CONSTRAINT chk_account_status CHECK (account_status IN ('active', 'inactive', 'suspended'))
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_status ON customers(account_status);

CREATE TRIGGER update_customers_timestamp
    BEFORE UPDATE ON customers
    FOR EACH ROW
    EXECUTE FUNCTION update_driver_timestamp();

COMMENT ON TABLE customers IS 'Customer information with PII';