# Milestone #52: Build ETL Pipeline - Customers

**Your Role:** Data Engineer

Create `src/data_engineering/etl_customers.py`:
- Extract: Read `data/raw/customers.csv`
- Transform: Anonymize PII, handle duplicates
- Load: Insert into `customers` table
- Create DAG `dags/etl_customers_dag.py`
- Run and commit.