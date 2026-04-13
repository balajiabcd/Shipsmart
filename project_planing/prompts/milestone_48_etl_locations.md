# Milestone #48: Build ETL Pipeline - Locations

**Your Role:** Data Engineer

Create `src/data_engineering/etl_locations.py`:
- Extract: Read `data/raw/locations.csv`
- Transform: Fix geocoding issues, fill missing coordinates
- Load: Insert into `locations` table
- Create DAG `dags/etl_locations_dag.py`
- Run and commit.

---

### Milestone #48 Completed
- src/data_engineering/etl_locations.py (ETL pipeline for locations)
- Extracts from data/raw/locations.csv
- Transforms: fixes geocoding issues, fills missing coordinates
- Loads to locations table in database
- Next: Milestone #49