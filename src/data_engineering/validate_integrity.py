"""
Data Integrity Validation Script
"""

import os
from sqlalchemy import create_engine, text


def get_connection():
    """Create database connection."""
    conn_string = os.getenv(
        "DATABASE_URL", "postgresql://shipsmart:shipsmart2024@localhost:5432/shipsmart"
    )
    return create_engine(conn_string)


def validate_foreign_keys(engine):
    """Validate foreign key relationships."""
    print("\n=== Foreign Key Validation ===")
    issues = []

    checks = [
        (
            "orders -> customers",
            "SELECT COUNT(*) FROM orders o WHERE o.customer_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id)",
        ),
        (
            "orders -> drivers",
            "SELECT COUNT(*) FROM orders o WHERE o.driver_id IS NOT NULL AND o.driver_id != 'UNKNOWN' AND NOT EXISTS (SELECT 1 FROM drivers d WHERE d.driver_id = o.driver_id)",
        ),
        (
            "orders -> warehouses",
            "SELECT COUNT(*) FROM orders o WHERE o.warehouse_id IS NOT NULL AND o.warehouse_id != 'UNKNOWN' AND NOT EXISTS (SELECT 1 FROM warehouses w WHERE w.warehouse_id = o.warehouse_id)",
        ),
        (
            "delivery_events -> orders",
            "SELECT COUNT(*) FROM delivery_events de WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = de.order_id)",
        ),
        (
            "delivery_events -> drivers",
            "SELECT COUNT(*) FROM delivery_events de WHERE de.driver_id IS NOT NULL AND de.driver_id != 'UNKNOWN' AND NOT EXISTS (SELECT 1 FROM drivers d WHERE d.driver_id = de.driver_id)",
        ),
        (
            "delivery_events -> locations",
            "SELECT COUNT(*) FROM delivery_events de WHERE de.location_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM locations l WHERE l.location_id = de.location_id)",
        ),
        (
            "drivers_performance -> drivers",
            "SELECT COUNT(*) FROM drivers_performance dp WHERE NOT EXISTS (SELECT 1 FROM drivers d WHERE d.driver_id = dp.driver_id)",
        ),
        (
            "warehouse_performance -> warehouses",
            "SELECT COUNT(*) FROM warehouse_performance wp WHERE NOT EXISTS (SELECT 1 FROM warehouses w WHERE w.warehouse_id = wp.warehouse_id)",
        ),
    ]

    with engine.connect() as conn:
        for name, query in checks:
            try:
                result = conn.execute(text(query)).scalar()
                status = "FAIL" if result > 0 else "PASS"
                print(f"  {name}: {status} ({result} orphaned records)")
                if result > 0:
                    issues.append(f"{name}: {result} orphaned records")
            except Exception as e:
                print(f"  {name}: ERROR - {e}")

    return issues


def validate_duplicates(engine):
    """Check for duplicate records."""
    print("\n=== Duplicate Records Validation ===")
    issues = []

    tables = ["orders", "customers", "drivers", "vehicles", "warehouses", "routes"]

    with engine.connect() as conn:
        for table in tables:
            try:
                id_col = f"{table[:-1]}_id" if table.endswith("s") else f"{table}_id"
                query = f"SELECT COUNT(*) - COUNT(DISTINCT {id_col}) FROM {table}"
                result = conn.execute(text(query)).scalar()
                status = "FAIL" if result > 0 else "PASS"
                print(f"  {table}: {status} ({result} duplicates)")
                if result > 0:
                    issues.append(f"{table}: {result} duplicate IDs")
            except Exception as e:
                print(f"  {table}: ERROR - {e}")

    return issues


def validate_constraints(engine):
    """Check data constraints."""
    print("\n=== Data Constraints Validation ===")
    issues = []

    checks = [
        (
            "orders status values",
            "SELECT COUNT(*) FROM orders WHERE status NOT IN ('pending', 'in_transit', 'delivered', 'cancelled')",
        ),
        (
            "orders negative delays",
            "SELECT COUNT(*) FROM orders WHERE delay_minutes < 0",
        ),
        (
            "drivers rating range",
            "SELECT COUNT(*) FROM drivers WHERE rating < 0 OR rating > 5",
        ),
        ("vehicles capacity", "SELECT COUNT(*) FROM vehicles WHERE capacity_kg < 0"),
    ]

    with engine.connect() as conn:
        for name, query in checks:
            try:
                result = conn.execute(text(query)).scalar()
                status = "FAIL" if result > 0 else "PASS"
                print(f"  {name}: {status} ({result} violations)")
                if result > 0:
                    issues.append(f"{name}: {result} violations")
            except Exception as e:
                print(f"  {name}: ERROR - {e}")

    return issues


def validate_nulls(engine):
    """Check for unexpected nulls."""
    print("\n=== Null Value Validation ===")
    issues = []

    checks = [
        ("orders order_id", "SELECT COUNT(*) FROM orders WHERE order_id IS NULL"),
        ("orders order_time", "SELECT COUNT(*) FROM orders WHERE order_time IS NULL"),
        (
            "customers customer_id",
            "SELECT COUNT(*) FROM customers WHERE customer_id IS NULL",
        ),
        ("drivers driver_id", "SELECT COUNT(*) FROM drivers WHERE driver_id IS NULL"),
        (
            "vehicles vehicle_id",
            "SELECT COUNT(*) FROM vehicles WHERE vehicle_id IS NULL",
        ),
        (
            "warehouses warehouse_id",
            "SELECT COUNT(*) FROM warehouses WHERE warehouse_id IS NULL",
        ),
    ]

    with engine.connect() as conn:
        for name, query in checks:
            try:
                result = conn.execute(text(query)).scalar()
                status = "FAIL" if result > 0 else "PASS"
                print(f"  {name}: {status} ({result} nulls)")
                if result > 0:
                    issues.append(f"{name}: {result} null values")
            except Exception as e:
                print(f"  {name}: ERROR - {e}")

    return issues


def run_validation():
    """Run all validation checks."""
    print("=" * 50)
    print("Shipsmart Data Integrity Validation")
    print("=" * 50)

    try:
        engine = get_connection()
        print("\nDatabase connection established")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    all_issues = []
    all_issues.extend(validate_foreign_keys(engine))
    all_issues.extend(validate_duplicates(engine))
    all_issues.extend(validate_constraints(engine))
    all_issues.extend(validate_nulls(engine))

    print("\n" + "=" * 50)
    if all_issues:
        print(f"VALIDATION FAILED: {len(all_issues)} issues found")
        print("\nIssues:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("VALIDATION PASSED: No issues found")
    print("=" * 50)


if __name__ == "__main__":
    run_validation()
