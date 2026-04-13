# Shipsmart Data Simulation Plan

## Overview

This document defines the data simulation plan for generating synthetic logistics data with realistic errors, missing values, and inconsistencies for the Shipsmart delay prediction system.

---

## CSV Files to Generate (20 Files)

| # | File Name | Records | Key Fields | Data Quality Issues |
|---|-----------|---------|-------------|---------------------|
| 1 | orders.csv | 100,000 | order_id, customer_id, driver_id, warehouse_id, origin, destination, order_time, delivery_time, status | 3% missing values |
| 2 | drivers.csv | 500 | driver_id, name, license_number, vehicle_id, hire_date, status | Inconsistent date formats |
| 3 | vehicles.csv | 300 | vehicle_id, type, capacity, plate_number, maintenance_due | 2% outliers in capacity |
| 4 | warehouses.csv | 20 | warehouse_id, location, capacity, manager | 5% missing fields |
| 5 | routes.csv | 1,000 | route_id, origin, destination, distance, avg_duration | Duplicate entries |
| 6 | locations.csv | 500 | location_id, city, lat, long, region | Geocoding issues |
| 7 | weather.csv | 50,000 | date, location_id, temperature, condition, humidity | 10% null values |
| 8 | traffic.csv | 50,000 | date, route_id, congestion_level, avg_speed | Inconsistent data |
| 9 | holidays.csv | 500 | date, country, region, holiday_name | Format issues |
| 10 | customers.csv | 20,000 | customer_id, name, email, phone, address | PII data (anonymize) |
| 11 | delivery_events.csv | 200,000 | event_id, order_id, timestamp, event_type, location | Missing timestamps |
| 12 | drivers_performance.csv | 50,000 | driver_id, date, deliveries, on_time, late, rating | Historical data |
| 13 | warehouse_performance.csv | 5,000 | warehouse_id, date, throughput, delays, efficiency | Missing metrics |
| 14 | route_traffic_history.csv | 100,000 | route_id, date, time, traffic_level | Inconsistent levels |
| 15 | vehicle_maintenance.csv | 5,000 | vehicle_id, date, maintenance_type, cost, next_due | Random gaps |
| 16 | fuel_prices.csv | 10,000 | date, location, fuel_type, price | Outliers |
| 17 | customer_feedback.csv | 30,000 | order_id, customer_id, rating, comment, timestamp | Missing comments |
| 18 | competitor_data.csv | 1,000 | competitor_id, region, market_share, pricing | Limited data |
| 19 | delay_reasons.csv | 10,000 | delay_id, order_id, reason, severity, duration | Categorical issues |
| 20 | demand_forecasting.csv | 20,000 | date, region, predicted_demand, actual_demand | Forecast errors |

---

## Schema Definitions

### 1. orders.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| order_id | string | Unique order identifier | ORD-XXXXXXXX |
| customer_id | string | Foreign key to customers | CUST-XXXXX |
| driver_id | string | Foreign key to drivers | DRV-XXX |
| warehouse_id | string | Foreign key to warehouses | WH-XX |
| origin_location_id | string | Pickup location | LOC-XXX |
| destination_location_id | string | Delivery location | LOC-XXX |
| order_time | datetime | Order placement time | YYYY-MM-DD HH:MM:SS |
| scheduled_delivery_time | datetime | Expected delivery | YYYY-MM-DD HH:MM:SS |
| actual_delivery_time | datetime | Actual delivery | YYYY-MM-DD HH:MM:SS or NULL |
| status | string | Order status | pending, in_transit, delivered, delayed, cancelled |
| priority | string | Delivery priority | low, medium, high, urgent |
| package_weight | float | Weight in kg | 0.1 - 1000.0 |
| package_dimensions | string | LxWxH in cm | "LxWxH" |
| shipping_type | string | Service type | standard, express, overnight |
| estimated_cost | float | Estimated cost | 5.00 - 500.00 |
| delay_minutes | int | Delay in minutes | 0 - 480 or NULL |

**Data Quality Issues:**
- 3% missing values in driver_id, warehouse_id
- 2% inconsistent datetime formats
- 5% duplicate order_id entries

### 2. drivers.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| driver_id | string | Unique driver ID | DRV-XXX |
| first_name | string | Driver first name | Random names |
| last_name | string | Driver last name | Random names |
| license_number | string | License number | DL-XXXXXXXX |
| license_expiry | date | License expiry date | YYYY-MM-DD |
| vehicle_id | string | Assigned vehicle | VEH-XX or NULL |
| hire_date | date | Date of hire | YYYY-MM-DD or DD/MM/YYYY |
| status | string | Employment status | active, on_leave, suspended |
| contact_phone | string | Phone number | Various formats |
| email | string | Email address | driver@shipsmart.com |
| base_location | string | Home depot | WH-XX |
| rating | float | Performance rating | 1.0 - 5.0 |
| total_deliveries | int | Total deliveries | 0 - 10000 |
| on_time_rate | float | On-time percentage | 0.0 - 100.0 |

**Data Quality Issues:**
- Inconsistent date formats (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
- 2% missing email values
- 1% invalid license numbers

### 3. vehicles.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| vehicle_id | string | Unique vehicle ID | VEH-XX |
| vehicle_type | string | Vehicle category | van, truck, bike, scooter |
| make | string | Manufacturer | Mercedes, Ford, etc. |
| model | string | Model name | Sprinter, Transit, etc. |
| year | int | Manufacturing year | 2015 - 2024 |
| capacity_kg | float | Load capacity | 100 - 5000 |
| capacity_vol | float | Volume in m3 | 1 - 50 |
| plate_number | string | License plate | B-XX-XXXX |
| vin | string | Vehicle ID number | 17-char VIN |
| insurance_expiry | date | Insurance expiry | YYYY-MM-DD |
| maintenance_due | date | Next service due | YYYY-MM-DD |
| status | string | Availability | active, maintenance, retired |
| mileage | int | Total kilometers | 0 - 300000 |
| fuel_type | string | Fuel category | diesel, petrol, electric, hybrid |

**Data Quality Issues:**
- 2% outliers in capacity_kg (negative or absurdly high values)
- Inconsistent plate number formats
- 3% missing maintenance_due

### 4. warehouses.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| warehouse_id | string | Unique warehouse ID | WH-XX |
| name | string | Warehouse name | Berlin Central, Munich Hub, etc. |
| location_id | string | Physical location | LOC-XXX |
| address | string | Full address | Street, City, Country |
| capacity_sqm | float | Storage capacity | 1000 - 50000 |
| manager_name | string | Manager name | Random names |
| manager_contact | string | Contact phone | +49XXX... |
| operations_start | time | Opening time | HH:MM |
| operations_end | time | Closing time | HH:MM |
| status | string | Operational status | active, closed, expansion |
| region | string | Geographic region | North, South, East, West |
| zone | string | Zone classification | A, B, C |

**Data Quality Issues:**
- 5% missing manager_contact
- Inconsistent zone classifications
- 2% missing capacity values

### 5. routes.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| route_id | string | Unique route ID | RTE-XXXX |
| origin_location_id | string | Start point | LOC-XXX |
| destination_location_id | string | End point | LOC-XXX |
| distance_km | float | Distance | 1 - 1000 |
| avg_duration_minutes | int | Average time | 10 - 720 |
| route_type | string | Route category | highway, urban, mixed |
| toll_roads | boolean | Has tolls | true, false |
| traffic_rating | string | Traffic level | low, medium, high |
| preferred_times | string | Best departure | morning, afternoon, evening |
| alternate_route_id | string | Alternative route | RTE-XXXX or NULL |

**Data Quality Issues:**
- 3% duplicate route entries (same origin/dest)
- Inconsistent distance units (km vs miles)
- 2% missing avg_duration

### 6. locations.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| location_id | string | Unique location ID | LOC-XXX |
| location_type | string | Type | residential, commercial, industrial |
| street_address | string | Street address | Random addresses |
| city | string | City name | German cities |
| state | string | State/Region | Bavaria, Berlin, etc. |
| postal_code | string | Postal code | 5-digit |
| country | string | Country | Germany |
| latitude | float | GPS latitude | 47.0 - 55.0 |
| longitude | float | GPS longitude | 5.0 - 15.0 |
| region | string | Geographic region | North, South, East, West |
| timezone | string | Timezone | Europe/Berlin |
| geocoding_status | string | Geocoding quality | exact, approximate, manual |

**Data Quality Issues:**
- 5% geocoding issues (approx coordinates)
- 2% missing postal codes
- Inconsistent city names (variations)

### 7. weather.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| date | datetime | Date/time | YYYY-MM-DD HH:MM |
| location_id | string | Location | LOC-XXX |
| temperature_celsius | float | Temperature | -20 to 40 |
| feels_like_celsius | float | Apparent temp | -25 to 45 |
| humidity_percent | int | Humidity | 0 - 100 |
| wind_speed_kmh | float | Wind speed | 0 - 150 |
| wind_direction | string | Direction | N, NE, E, SE, S, SW, W, NW |
| condition | string | Weather state | clear, cloudy, rain, snow, fog, storm |
| visibility_km | float | Visibility | 0.1 - 50 |
| pressure_hpa | int | Barometric pressure | 950 - 1050 |
| uv_index | int | UV index | 0 - 11 |
| precipitation_mm | float | Rainfall | 0 - 100 |

**Data Quality Issues:**
- 10% null values in humidity, wind columns
- Inconsistent condition values
- 2% temperature outliers

### 8. traffic.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| date | datetime | Date/time | YYYY-MM-DD HH:MM |
| route_id | string | Route | RTE-XXXX |
| congestion_level | string | Traffic level | none, light, moderate, heavy, severe |
| avg_speed_kmh | float | Average speed | 0 - 200 |
| traffic_volume | int | Vehicles/hour | 0 - 10000 |
| incident_reported | boolean | accidents | true, false |
| delay_minutes | int | Added delay | 0 - 120 |

**Data Quality Issues:**
- Inconsistent congestion_level values
- 5% missing avg_speed
- 2% duplicate entries

### 9. holidays.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| date | date | Holiday date | YYYY-MM-DD |
| country | string | Country | Germany |
| region | string | State/Region | Bavaria, Berlin, etc. |
| holiday_name | string | Holiday name | Christmas, Easter, etc. |
| holiday_type | string | Type | national, regional, observance |
| celebrations | int | Expected turnout | 1000 - 100000 |

**Data Quality Issues:**
- Inconsistent date formats
- Duplicate holiday entries
- Missing region for national holidays

### 10. customers.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| customer_id | string | Unique ID | CUST-XXXXX |
| first_name | string | Customer first name | Random names |
| last_name | string | Customer last name | Random names |
| email | string | Email address | email@example.com |
| phone | string | Phone number | Various formats |
| address | string | Full address | Street, City, Postal |
| location_id | string | Reference | LOC-XXX |
| customer_since | date | Registration date | YYYY-MM-DD |
| customer_type | string | Category | individual, business |
| credit_limit | float | Credit limit | 0 - 10000 |
| preferred_shipping | string | Service type | standard, express |
| account_status | string | Status | active, inactive, suspended |

**Data Quality Issues:**
- PII data needs anonymization
- 5% missing phone numbers
- Inconsistent email formats

### 11. delivery_events.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| event_id | string | Unique event ID | EVT-XXXXXXXX |
| order_id | string | Order reference | ORD-XXXXXXXX |
| event_timestamp | datetime | Event time | YYYY-MM-DD HH:MM:SS |
| event_type | string | Event category | created, pickup, in_transit, out_for_delivery, delivered, failed_attempt |
| location_id | string | Location | LOC-XXX |
| latitude | float | GPS latitude | 47.0 - 55.0 |
| longitude | float | GPS longitude | 5.0 - 15.0 |
| driver_id | string | Driver (if applicable) | DRV-XXX or NULL |
| notes | string | Event notes | Free text |
| temperature | float | Temp at location | -10 to 40 |

**Data Quality Issues:**
- 8% missing timestamps (use order_time as proxy)
- 3% missing location
- Inconsistent event_type values

### 12. drivers_performance.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| driver_id | string | Driver ID | DRV-XXX |
| performance_date | date | Record date | YYYY-MM-DD |
| total_deliveries | int | Daily deliveries | 0 - 50 |
| on_time_deliveries | int | On-time count | 0 - total |
| late_deliveries | int | Late count | 0 - total |
| failed_deliveries | int | Failed count | 0 - 10 |
| customer_ratings_sum | float | Total ratings | 0 - 250 |
| customer_ratings_count | int | Rating count | 0 - 50 |
| avg_delivery_time_minutes | float | Average time | 10 - 120 |
| fuel_efficiency | float | km per liter | 5 - 25 |
| accidents | int | Accident count | 0 - 5 |
| customer_complaints | int | Complaint count | 0 - 10 |

**Data Quality Issues:**
- Missing data for some driver-date combinations
- Inconsistent rating scales
- 2% negative delivery counts

### 13. warehouse_performance.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| warehouse_id | string | Warehouse ID | WH-XX |
| performance_date | date | Record date | YYYY-MM-DD |
| inbound_volume | int | Packages received | 0 - 5000 |
| outbound_volume | int | Packages shipped | 0 - 5000 |
| processing_time_avg | float | Avg processing min | 5 - 60 |
| delays_count | int | Delay incidents | 0 - 100 |
| efficiency_score | float | Efficiency % | 50 - 100 |
| staff_count | int | Workers on duty | 5 - 200 |
| overtime_hours | float | Overtime total | 0 - 500 |
| throughput_per_hour | float | Packages/hour | 10 - 200 |
| error_rate | float | Error percentage | 0 - 10 |
| returns_received | int | Return count | 0 - 500 |

**Data Quality Issues:**
- 10% missing efficiency_score
- Inconsistent throughput values
- 3% negative counts

### 14. route_traffic_history.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| route_id | string | Route ID | RTE-XXXX |
| record_date | date | Date | YYYY-MM-DD |
| hour | int | Hour of day | 0 - 23 |
| traffic_level | string | Level | low, medium, high, severe |
| avg_congestion | float | 0-1 scale | 0.0 - 1.0 |
| avg_speed | float | km/h | 0 - 200 |
| travel_time_multiplier | float | Time factor | 1.0 - 5.0 |
| incidents_count | int | Incidents | 0 - 10 |

**Data Quality Issues:**
- Inconsistent traffic_level values (variations)
- 5% missing avg_speed
- Duplicate entries

### 15. vehicle_maintenance.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| vehicle_id | string | Vehicle ID | VEH-XX |
| maintenance_date | date | Service date | YYYY-MM-DD |
| maintenance_type | string | Service type | oil_change, tire_rotation, brake_service, inspection, repair |
| description | string | Work description | Free text |
| cost | float | Service cost | 50 - 5000 |
| mechanic_id | string | Mechanic | MECH-XX |
| parts_replaced | string | Parts list | comma-separated |
| next_maintenance_due | date | Next service | YYYY-MM-DD |
| mileage_at_service | int | Odometer reading | 0 - 300000 |
| service_duration_hours | float | Time spent | 1 - 48 |
| warranty_claim | boolean | Warranty | true, false |

**Data Quality Issues:**
- Random gaps in maintenance history
- 3% missing cost
- Inconsistent maintenance_type values

### 16. fuel_prices.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| date | date | Record date | YYYY-MM-DD |
| location_id | string | Location | LOC-XXX |
| fuel_type | string | Fuel category | diesel, petrol, e5, e10, electric |
| price_per_liter | float | Price in EUR | 1.0 - 3.0 |
| station_name | string | Station | Shell, BP, etc. |
| station_brand | string | Brand | Various |

**Data Quality Issues:**
- 2% price outliers
- Missing prices for some locations
- Inconsistent fuel_type values

### 17. customer_feedback.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| feedback_id | string | Unique ID | FD-XXXXXXXX |
| order_id | string | Order reference | ORD-XXXXXXXX |
| customer_id | string | Customer | CUST-XXXXX |
| rating | int | Star rating | 1 - 5 |
| comment | string | Feedback text | Free text or NULL |
| feedback_date | datetime | Submission time | YYYY-MM-DD HH:MM |
| feedback_type | string | Type | delivery, packaging, service |
| would_recommend | boolean | NPS question | true, false |

**Data Quality Issues:**
- 30% missing comments
- 2% invalid ratings (0 or >5)
- Duplicate feedback

### 18. competitor_data.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| competitor_id | string | Competitor ID | COMP-XX |
| competitor_name | string | Company name | DHL, UPS, etc. |
| region | string | Operating region | North, South, East, West |
| market_share_percent | float | Market share | 0 - 50 |
| avg_delivery_time | float | Days to deliver | 1 - 7 |
| price_index | float | Price vs market | 0.8 - 1.5 |
| service_rating | float | Rating | 1.0 - 5.0 |
| coverage_cities | int | Cities served | 10 - 500 |
| data_date | date | Data collection | YYYY-MM-DD |

**Data Quality Issues:**
- Limited historical data
- 10% missing ratings
- Inconsistent regions

### 19. delay_reasons.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| delay_id | string | Unique ID | DLY-XXXXX |
| order_id | string | Order reference | ORD-XXXXXXXX |
| reason | string | Delay cause | traffic, weather, warehouse, driver, custom |
| severity | string | Impact level | low, medium, high, critical |
| duration_minutes | int | Delay minutes | 5 - 480 |
| reported_by | string | Source | system, driver, customer |
| timestamp | datetime | Report time | YYYY-MM-DD HH:MM |
| resolved | boolean | Resolution status | true, false |
| resolution_minutes | int | Resolution time | 0 - 120 |

**Data Quality Issues:**
- Inconsistent reason values
- 5% missing severity
- Duplicate delay entries

### 20. demand_forecasting.csv

| Column | Type | Description | Range/Format |
|--------|------|------------|--------------|
| forecast_date | date | Forecast date | YYYY-MM-DD |
| region | string | Geographic region | North, South, East, West |
| predicted_demand | int | Forecasted orders | 100 - 10000 |
| actual_demand | int | Actual orders | 100 - 10000 or NULL |
| forecast_accuracy | float | Accuracy % | 0 - 100 |
| model_version | string | Model used | v1, v2, v3 |
| forecast_horizon_days | int | Days ahead | 1 - 14 |
| seasonal_factor | float | Seasonal adj | 0.5 - 2.0 |
| weather_impact | float | Weather effect | -0.5 - 0.5 |
| holiday_impact | float | Holiday effect | 0.0 - 1.0 |

**Data Quality Issues:**
- Inconsistent region names
- 20% missing actual_demand
- 5% negative demand values

---

## Data Quality Issues Summary

| Issue Type | Files Affected | Rate |
|-----------|----------------|------|
| Missing values | orders, drivers, weather, delivery_events | 3-10% |
| Outliers | vehicles, fuel_prices, demand | 2-5% |
| Inconsistent formats | drivers, holidays, routes, traffic | Common |
| Duplicates | orders, routes, traffic, feedback | 1-3% |
| PII concerns | customers | Requires anonymization |
| Invalid categories | delay_reasons, weather | 2-5% |
| Gaps | vehicle_maintenance, drivers_performance | Random |

---

## Generation Strategy

1. **Base Data Generation**: Generate clean data first
2. **Introduce Errors**: Apply quality issues programmatically
3. **Cross-file Validation**: Ensure foreign key integrity
4. **Randomization**: Add realistic randomness
5. **Validation**: Verify approximate statistics

---

*Document Version: 1.0*
*Created: April 2026*
*Project: Shipsmart - The Smart Supply Chain*