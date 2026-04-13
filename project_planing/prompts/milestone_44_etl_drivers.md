# Milestone #44: Build ETL Pipeline - Drivers

**Your Role:** Data Engineer

Create `src/data_engineering/etl_drivers.py`:
- Extract: Read `data/raw/drivers.csv`
- Transform: Standardize date formats, handle missing license numbers
- Load: Insert into `drivers` table
- Create Airflow DAG `dags/etl_drivers_dag.py`
- Run and commit.

---

### Milestone #44 Completed
- src/data_engineering/etl_drivers.py (ETL pipeline for drivers)
- Extracts from data/raw/drivers.csv
- Transforms: date formats, license validation, performance score calculation
- Loads to drivers table in database
- Next: Milestone #45