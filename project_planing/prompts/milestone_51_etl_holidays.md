# Milestone #51: Build ETL Pipeline - Holidays

**Your Role:** Data Engineer

Create `src/data_engineering/etl_holidays.py`:
- Extract: Read `data/raw/holidays.csv`
- Transform: Standardize date formats
- Load: Insert into `holidays` table
- Create DAG `dags/etl_holidays_dag.py`
- Run and commit.

---

### Milestone #51 Completed
- src/data_engineering/etl_holidays.py (ETL pipeline for holidays)
- Extracts from data/raw/holidays.csv
- Transforms: standardizes date formats
- Loads to holidays table in database
- Next: Milestone #52