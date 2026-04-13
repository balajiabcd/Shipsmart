# Milestone #54: Build ETL Pipeline - Performance Data

**Your Role:** Data Engineer

Create `src/data_engineering/etl_performance.py`:
- Extract: Read `data/raw/drivers_performance.csv` and `data/raw/warehouse_performance.csv`
- Transform: Handle missing ratings, outliers
- Load: Insert into `drivers_performance` and `warehouse_performance` tables
- Create DAG `dags/etl_performance_dag.py`
- Run and commit.