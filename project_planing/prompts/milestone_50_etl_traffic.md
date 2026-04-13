# Milestone #50: Build ETL Pipeline - Traffic

**Your Role:** Data Engineer

Create `src/data_engineering/etl_traffic.py`:
- Extract: Read `data/raw/traffic.csv`
- Transform: Standardize congestion levels
- Load: Insert into `traffic` table
- Create DAG `dags/etl_traffic_dag.py`
- Run and commit.

---

### Milestone #50 Completed
- src/data_engineering/etl_traffic.py (ETL pipeline for traffic)
- Extracts from data/raw/traffic.csv
- Transforms: standardizes congestion levels
- Loads to traffic table in database
- Next: Milestone #51