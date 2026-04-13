# Milestone #47: Build ETL Pipeline - Routes

**Your Role:** Data Engineer

Create `src/data_engineering/etl_routes.py`:
- Extract: Read `data/raw/routes.csv`
- Transform: Handle duplicates, missing durations
- Load: Insert into `routes` table
- Create DAG `dags/etl_routes_dag.py`
- Run and commit.