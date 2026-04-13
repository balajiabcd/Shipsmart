# Milestone #49: Build ETL Pipeline - Weather

**Your Role:** Data Engineer

Create `src/data_engineering/etl_weather.py`:
- Extract: Read `data/raw/weather.csv`
- Transform: Handle 10% null temperatures, 8% null humidity
- Load: Insert into `weather` table
- Create DAG `dags/etl_weather_dag.py`
- Run and commit.

---

### Milestone #49 Completed
- src/data_engineering/etl_weather.py (ETL pipeline for weather)
- Extracts from data/raw/weather.csv
- Transforms: handles 10% null temps, 8% null humidity
- Loads to weather table in database
- Next: Milestone #50