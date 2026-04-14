# Shipsmart Data Dictionary

## Overview

This document describes all columns in the Shipsmart raw CSV files.

## orders.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| order_id | string | Unique order identifier | ORD-00000001 |
| customer_id | string | FK to customers | CUST-015796 |
| driver_id | string | FK to drivers (nullable) | DRV-0006 |
| warehouse_id | string | FK to warehouses (nullable) | WH-01 |
| origin_location | float | Origin latitude | 49.4542 |
| origin_longitude | float | Origin longitude | 11.0775 |
| dest_location | float | Destination latitude | 48.1351 |
| dest_longitude | float | Destination longitude | 11.582 |
| order_time | datetime | Order placement time | 2024-12-26 23:44 |
| scheduled_delivery_time | datetime | Expected delivery | 2024-12-29 12:44 |
| actual_delivery_time | datetime | Actual delivery (nullable) | 2024-12-29 12:44 |
| status | string | Order status | pending, in_transit, delivered, cancelled |
| delay_minutes | int | Delay in minutes (nullable) | 0-240 |
| package_weight_kg | float | Package weight (nullable) | 66.16 |
| package_dimensions_*(cm) | int | L x W x H | 56,20,14 |
| package_type | string | Type | document, parcel, fragile, oversized |
| shipping_type | string | Service | standard, express, overnight |
| priority | string | Priority | low, medium, high, urgent |
| estimated_cost_eur | float | Estimated cost | 226.78 |
| actual_cost_eur | float | Actual cost | 294.51 |

## drivers.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| driver_id | string | Unique driver ID | DRV-0001 |
| full_name | string | Driver name | Hans Müller |
| license_number | string | License # (nullable) | DL-12345678 |
| license_expiry | date | Expiry date | 2026-12-31 |
| vehicle_id | string | Assigned vehicle (nullable) | VEH-001 |
| hire_date | date | Hire date (inconsistent formats) | 2020-05-15 |
| status | string | Employment status | active, on_leave, suspended |
| rating | float | Performance rating | 4.5 |
| total_deliveries | int | Total deliveries | 5000 |
| on_time_rate | float | On-time % | 0.85 |
| contact_phone | string | Phone number | +49151123456 |
| base_location | string | Home depot | WH-01 |

## vehicles.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| vehicle_id | string | Unique vehicle ID | VEH-001 |
| vehicle_type | string | Category | van, truck, motorcycle |
| make | string | Manufacturer | Mercedes |
| model | string | Model name | Sprinter |
| manufacturing_year | int | Year | 2020 |
| capacity_kg | float | Load capacity (outliers possible) | 1200.0 |
| plate_number | string | License plate | B-AB-123 |
| vin | string | Vehicle ID number | WDR1234567890 |
| insurance_expiry | date | Insurance expiry | 2025-06-30 |
| maintenance_due | date | Next service (nullable) | 2025-03-15 |
| status | string | Availability | active, maintenance, retired |
| mileage | int | Total km | 50000 |
| fuel_type | string | Fuel category | diesel, petrol, electric |

## warehouses.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| warehouse_id | string | Unique ID | WH-01 |
| warehouse_name | string | Name | Berlin Hub |
| city | string | City | Berlin |
| latitude | float | GPS latitude | 52.52 |
| longitude | float | GPS longitude | 13.405 |
| capacity_sqm | int | Storage capacity | 15000 |
| manager_name | string | Manager (nullable) | Hans Müller |
| manager_contact | string | Phone (nullable) | +4930123456 |
| email | string | Email (nullable) | warehouse1@shipsmart.de |
| established_date | date | Establishment date | 2018-01-15 |
| operating_hours | string | Hours | 06:00-22:00 |
| zone | string | Zone classification | A, B, C |
| region | string | Geographic region | North, South, East, West |
| status | string | Operational status | active, expansion, closed |

## routes.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| route_id | string | Unique route ID | RTE-0001 |
| origin_city | string | Start city | Berlin |
| destination_city | string | End city | Munich |
| distance_km | float | Distance | 580.5 |
| avg_duration_minutes | int | Average time (nullable) | 360 |
| route_type | string | Category | highway, secondary, local, mixed, urban, unknown |
| traffic_level | string | Traffic level | low, medium, high |
| toll_roads | bool | Has tolls | true, false |
| preferred_times | string | Best departure | morning, afternoon, evening, any |

## locations.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| location_id | string | Unique ID | LOC-0001 |
| city | string | City name | Berlin |
| latitude | float | GPS (nullable for geocoding issues) | 52.52 |
| longitude | float | GPS (nullable for geocoding issues) | 13.405 |
| region | string | Region | North, South, East, West, Central |
| population | int | City population | 3645000 |
| location_type | string | Type | residential, commercial, industrial |
| postal_code | string | Postal code | 10115 |

## weather.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| timestamp | datetime | Date/time | 2024-12-26 14:00 |
| location_city | string | City | Berlin |
| temperature_celsius | float (nullable) | Temperature | 5.2 |
| humidity_percent | float (nullable) | Humidity | 75.3 |
| wind_speed_kmh | float (nullable) | Wind speed | 25.5 |
| wind_direction | string | Direction | NE, E, SE, S, SW, W, NW |
| condition | string | Weather state | clear, cloudy, rain, snow, fog, storm |
| visibility_km | float | Visibility | 10.0 |

## traffic.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| timestamp | datetime | Date/time | 2024-12-26 14:00 |
| route_id | string | Route | RTE-0001 |
| hour | int | Hour of day | 14 |
| congestion_level | string | Level (includes unknown) | low, medium, high, severe |
| avg_speed_kmh | float (nullable) | Average speed | 85.5 |
| traffic_volume | int | Vehicles/hour | 2500 |
| delay_minutes | int | Added delay | 15 |

## holidays.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| date | date | Holiday date (inconsistent formats) | 2024-12-25 |
| country | string | Country | Germany |
| region | string | State (nullable) | Berlin |
| holiday_name | string | Holiday name | Christmas Day |
| holiday_type | string | Type | national, regional, movable |
| celebrations_expected | int | Expected turnout | 50000 |

## customers.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| customer_id | string | Unique ID | CUST-00001 |
| first_name | string | First name | Hans |
| last_name | string | Last name | Müller |
| email | string | Email address | hans.mueller@example.com |
| phone | string | Phone (nullable) | +49301234567 |
| street_address | string | Street address | Hauptstr. 123 |
| city | string | City | Berlin |
| postal_code | string | Postal code | 10115 |
| customer_since | date | Registration date | 2020-01-15 |
| customer_type | string | Category | individual, business |
| credit_limit | int | Credit limit | 1000 |
| preferred_shipping | string | Service | standard, express |
| account_status | string | Status | active, inactive |

## delivery_events.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| event_id | string | Unique ID | EVT-00000001 |
| order_id | string | Order reference | ORD-00000001 |
| timestamp | datetime (nullable) | Event time | 2024-12-26 14:30 |
| event_type | string | Category | created, picked_up, in_transit, delivered |
| location_id | string | Location (nullable) | LOC-0001 |
| driver_id | string | Driver | DRV-0001 |
| notes | string | Notes | Left at door |

## drivers_performance.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| driver_id | string | Driver ID | DRV-0001 |
| date | date | Record date | 2024-12-26 |
| total_deliveries | int | Daily deliveries | 25 |
| on_time_deliveries | int | On-time count | 20 |
| late_deliveries | int | Late count | 5 |
| rating | float (nullable) | Rating | 4.2 |
| customer_complaints | int (nullable) | Complaints | 1 |
| fuel_efficiency | float | km per liter | 12.5 |
| accidents | int | Accident count | 0 |
| overtime_hours | float | Overtime | 2.5 |

## warehouse_performance.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| warehouse_id | string | Warehouse ID | WH-01 |
| date | date | Record date | 2024-12-26 |
| inbound_volume | int | Packages received | 200 |
| outbound_volume | int | Packages shipped | 180 |
| throughput | int | Processed (outliers possible) | 180 |
| avg_processing_time_minutes | float | Average time | 25.5 |
| delays_count | int | Delay incidents | 3 |
| efficiency_score | float (nullable) | Efficiency % | 85.2 |
| staff_count | int | Workers on duty | 25 |
| overtime_hours | float | Overtime total | 50.0 |
| error_rate | float | Error % | 1.2 |
| returns_received | int | Return count | 15 |

## route_traffic_history.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| route_id | string | Route ID | RTE-0001 |
| date | date | Date | 2024-12-26 |
| hour | int | Hour | 14 |
| traffic_level | string | Level (includes unknown) | medium |
| avg_speed_kmh | float (nullable) | Speed | 75.0 |
| travel_time_multiplier | float | Time factor | 1.5 |
| incidents_count | int | Incidents | 0 |

## vehicle_maintenance.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| vehicle_id | string | Vehicle ID | VEH-001 |
| maintenance_date | date | Service date | 2024-12-01 |
| maintenance_type | string | Type | oil_change, tire_rotation |
| cost | float | Service cost | 150.0 |
| description | string | Work (nullable) | Routine oil change |
| mechanic_id | string | Mechanic | MECH-001 |
| mileage_at_service | int | Odometer reading | 75000 |
| next_maintenance_due | date (nullable) | Next service | 2025-06-01 |
| service_duration_hours | float | Time spent | 2.5 |

## fuel_prices.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| date | date | Date | 2024-12-26 |
| location | string | City | Berlin |
| fuel_type | string | Fuel | diesel, petrol, e5, e10, electric |
| price_per_liter | float | Price (outliers possible) | 1.55 |
| station_brand | string | Brand | Shell, BP |

## customer_feedback.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| feedback_id | string | Unique ID | FD-00000001 |
| order_id | string | Order | ORD-00000001 |
| customer_id | string | Customer | CUST-00001 |
| rating | int | Rating | 4 |
| comment | string (40% nullable) | Feedback | Great delivery! |
| feedback_date | datetime (nullable) | Time | 2024-12-26 14:30 |
| feedback_type | string | Type | delivery, packaging, service |
| would_recommend | bool | NPS | true |

## competitor_data.csv

| Column | Type | Description | Sample |
|--------|------|-------------|--------|
| competitor_id | string | ID | COMP-001 |
| competitor_name | string | Company | DHL |
| region | string | Region | North |
| market_share_percent | float (nullable) | Share | 15.5 |
| avg_delivery_time_days | float | Days | 2.5 |
| pricing_tier | string | Tier | standard |
| service_rating | float | Rating | 4.2 |
| coverage_cities | int | Cities | 250 |
| data_date | date | Data date | 2024-06-15 |

---

*Document Version: 1.0*
*Project: Shipsmart - Data Engineering* 
