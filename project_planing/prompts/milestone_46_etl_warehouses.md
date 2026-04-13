# Milestone #46: Build ETL Pipeline - Warehouses

**Your Role:** Data Engineer

Create `src/data_engineering/etl_warehouses.py`:
- Extract: Read `data/raw/warehouses.csv`
- Transform: Fill missing manager names, phones
- Load: Insert into `warehouses` table
- Create DAG `dags/etl_warehouses_dag.py`
- Run and commit.