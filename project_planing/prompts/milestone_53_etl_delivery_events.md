# Milestone #53: Build ETL Pipeline - Delivery Events

**Your Role:** Data Engineer

Create `src/data_engineering/etl_delivery_events.py`:
- Extract: Read `data/raw/delivery_events.csv`
- Transform: Handle missing timestamps
- Load: Insert into `delivery_events` table
- Create DAG `dags/etl_delivery_events_dag.py`
- Run and commit.