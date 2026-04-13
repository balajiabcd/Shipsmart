# Milestone #57: Validate Data Integrity

**Your Role:** Data Engineer

Create `src/data_engineering/validate_integrity.py`:
```python
from sqlalchemy import create_engine, text

def validate_integrity():
    engine = create_engine('postgresql://shipsmart:changeme@localhost:5432/shipsmart')
    
    checks = [
        # Check foreign keys
        "SELECT COUNT(*) FROM orders o WHERE o.customer_id NOT IN (SELECT customer_id FROM customers)",
        "SELECT COUNT(*) FROM orders o WHERE o.driver_id IS NOT NULL AND o.driver_id NOT IN (SELECT driver_id FROM drivers)",
        
        # Check duplicates
        "SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM orders",
        
        # Check constraints
        "SELECT COUNT(*) FROM orders WHERE status NOT IN ('pending', 'in_transit', 'delivered', 'cancelled')",
    ]
    
    with engine.connect() as conn:
        for check in checks:
            result = conn.execute(text(check)).scalar()
            print(f"{check[:50]}... : {result}")
    
    print("Data integrity validation complete")

validate_integrity()
```

Run and fix any issues. Commit.