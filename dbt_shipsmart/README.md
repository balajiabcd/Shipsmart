# DBT Project Configuration for Shipsmart

## Installation
```bash
pip install dbt-postgres
```

## Initialize DBT Project
```bash
dbt init dbt_shipsmart
```

## Project Structure
```
dbt_shipsmart/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── dim_customers.sql
│   ├── dim_orders.sql
│   ├── dim_drivers.sql
│   ├── dim_warehouses.sql
│   └── fct_delivery_metrics.sql
└── macros/
```

## profiles.yml Configuration
```yaml
shipsmart:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: shipsmart
      password: shipsmart2024
      dbname: shipsmart
      schema: dbt_dev
    prod:
      type: postgres
      host: localhost
      port: 5432
      user: shipsmart
      password: shipsmart2024
      dbname: shipsmart
      schema: dbt_prod
```

## Run DBT Commands
```bash
cd dbt_shipsmart
dbt debug          # Test connection
dbt run            # Run all models
dbt test           # Run tests
dbt docs generate # Generate docs
```

## Models

### Dimension Models
- **dim_customers**: Customer dimension with aggregations
- **dim_orders**: Order dimension with time attributes
- **dim_drivers**: Driver dimension with performance metrics
- **dim_warehouses**: Warehouse dimension with capacity info

### Fact Models
- **fct_delivery_metrics**: Delivery performance metrics (on-time rate, delays, etc.)

## Testing
Add tests in `schema.yml` for each model:
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
```