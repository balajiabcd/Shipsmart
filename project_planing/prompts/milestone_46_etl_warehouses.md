# Milestone #46: Build ETL Pipeline - Warehouses

**Your Role:** Data Engineer

Create `src/data_engineering/etl_warehouses.py`:
- Extract: Read `data/raw/warehouses.csv`
- Transform: Fill missing manager names, phones
- Load: Insert into `warehouses` table
- Create DAG `dags/etl_warehouses_dag.py`
- Run and commit.

---

### Milestone #46 Completed
- src/data_engineering/etl_warehouses.py (ETL pipeline for warehouses)
- Extracts from data/raw/warehouses.csv
- Transforms: fills missing manager names, contacts
- Loads to warehouses table in database
- Next: Milestone #47