# Milestone #45: Build ETL Pipeline - Vehicles

**Your Role:** Data Engineer

Create `src/data_engineering/etl_vehicles.py`:
- Extract: Read `data/raw/vehicles.csv`
- Transform: Handle capacity outliers, missing maintenance dates
- Load: Insert into `vehicles` table
- Create Airflow DAG `dags/etl_vehicles_dag.py`
- Run and commit.

---

### Milestone #45 Completed
- src/data_engineering/etl_vehicles.py (ETL pipeline for vehicles)
- Extracts from data/raw/vehicles.csv
- Transforms: capacity handling, maintenance/insurance status, vehicle age
- Loads to vehicles table in database
- ETL pipelines 36-45 complete!