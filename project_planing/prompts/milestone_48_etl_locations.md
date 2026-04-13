# Milestone #48: Build ETL Pipeline - Locations

**Your Role:** Data Engineer

Create `src/data_engineering/etl_locations.py`:
- Extract: Read `data/raw/locations.csv`
- Transform: Fix geocoding issues, fill missing coordinates
- Load: Insert into `locations` table
- Create DAG `dags/etl_locations_dag.py`
- Run and commit.