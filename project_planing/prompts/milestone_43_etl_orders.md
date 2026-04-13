# Milestone #43: Build ETL Pipeline - Orders

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #42 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Load and Clean Orders Data

**Your Role:** Data Engineer

**Instructions:**
1. Create ETL script `src/data_engineering/etl_orders.py`:
   ```python
   import pandas as pd
   from sqlalchemy import create_engine
   
   def etl_orders():
       # Extract
       df = pd.read_csv('data/raw/orders.csv')
       
       # Transform
       # Handle missing values
       df['driver_id'].fillna('UNKNOWN', inplace=True)
       df['warehouse_id'].fillna('UNKNOWN', inplace=True)
       
       # Clean dates
       df['order_time'] = pd.to_datetime(df['order_time'], errors='coerce')
       df['delivery_promise'] = pd.to_datetime(df['delivery_promise'], errors='coerce')
       
       # Remove invalid dates
       df = df[df['order_time'].notna()]
       
       # Load
       engine = create_engine('postgresql://shipsmart:changeme@localhost:5432/shipsmart')
       df.to_sql('orders', engine, if_exists='replace', index=False)
       print(f"Loaded {len(df)} orders to database")
   
   if __name__ == '__main__':
       etl_orders()
   ```

2. Create Airflow DAG `dags/etl_orders_dag.py`
3. Run ETL and verify
4. Commit and push

---

## Section 3: Instructions for Next AI Agent

*(Empty)*