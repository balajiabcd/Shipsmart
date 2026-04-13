# Shipsmart Data Pipeline Documentation

## Overview
This document describes the ETL pipelines and data flow for the Shipsmart logistics delay prediction system.

## Data Sources
- **Raw CSV files**: `data/raw/` - Contains all source data files (orders, drivers, vehicles, etc.)
- **External APIs**: Weather, Traffic, Holidays (to be integrated)

## ETL Pipelines
Each pipeline consists of:
1. **Extract**: Load from source (CSV/API)
2. **Transform**: Clean, validate, transform
3. **Load**: Insert into PostgreSQL

### Pipeline List
| Pipeline | Source | Destination | Frequency |
|----------|--------|-------------|-----------|
| orders_etl | orders.csv | orders table | Daily |
| drivers_etl | drivers.csv | drivers table | Daily |
| vehicles_etl | vehicles.csv | vehicles table | Daily |
| warehouses_etl | warehouses.csv | warehouses table | Daily |
| routes_etl | routes.csv | routes table | Daily |
| locations_etl | locations.csv | locations table | Daily |
| weather_etl | weather.csv | weather table | Daily |
| traffic_etl | traffic.csv | traffic table | Daily |
| holidays_etl | holidays.csv | holidays table | Daily |
| customers_etl | customers.csv | customers table | Daily |
| delivery_events_etl | delivery_events.csv | delivery_events table | Daily |
| performance_etl | drivers_performance.csv, warehouse_performance.csv | performance tables | Daily |

## Database Schema

### Core Tables
- `orders` - Main orders data
- `customers` - Customer information (PII anonymized)
- `drivers` - Driver details
- `vehicles` - Vehicle information
- `warehouses` - Warehouse locations

### Reference Tables
- `routes` - Route definitions
- `locations` - Geographic locations
- `weather` - Weather data
- `traffic` - Traffic data
- `holidays` - Holiday calendar

### Performance Tables
- `delivery_events` - Order delivery events
- `drivers_performance` - Driver daily metrics
- `warehouse_performance` - Warehouse daily metrics

## Database Views
Located in `database/views.sql`:
- `v_orders_details` - Orders with customer/driver joins
- `v_delayed_orders` - All delayed orders
- `v_daily_driver_performance` - Driver daily metrics
- `v_daily_warehouse_performance` - Warehouse daily metrics
- `v_delivery_timeline` - Order event timeline
- `v_customer_order_summary` - Customer order stats

## Database Indexes
Located in `database/indexes.sql`:
- Performance indexes on foreign keys
- Composite indexes for common queries
- Date/time indexes for time-series queries

## Airflow DAGs
All DAGs are in `dags/` directory and run on schedule:
- `shipsmart_etl.py` - Main ETL orchestration

## Data Quality
- Validation scripts in `src/data_engineering/validate_integrity.py`
- Automated checks in Airflow
- Foreign key validation
- Duplicate checks
- Constraint validation

## ETL Scripts Location
- `src/data_engineering/etl_*.py` - Individual ETL pipelines

## Troubleshooting

### Common Issues
1. **Missing data**: Check source CSV files exist
2. **Type errors**: Verify data types in transform functions
3. **Connection issues**: Check DATABASE_URL environment variable
4. **Foreign key failures**: Run validation script to identify orphaned records

### Run Validation
```bash
python src/data_engineering/validate_integrity.py
```

### Re-run ETL
```bash
python src/data_engineering/etl_orders.py
```