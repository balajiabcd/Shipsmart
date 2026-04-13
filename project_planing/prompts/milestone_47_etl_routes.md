# Milestone #47: Build ETL Pipeline - Routes

**Your Role:** Data Engineer

Create `src/data_engineering/etl_routes.py`:
- Extract: Read `data/raw/routes.csv`
- Transform: Handle duplicates, missing durations
- Load: Insert into `routes` table
- Create DAG `dags/etl_routes_dag.py`
- Run and commit.

---

### Milestone #47 Completed
- src/data_engineering/etl_routes.py (ETL pipeline for routes)
- Extracts from data/raw/routes.csv
- Transforms: handles duplicates, fills missing durations
- Loads to routes table in database
- Next: Milestone #48