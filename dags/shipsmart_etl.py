"""
Shipsmart ETL DAGs
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "shipsmart",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Main ETL DAG
etl_dag = DAG(
    "shipsmart_etl",
    default_args=default_args,
    description="Shipsmart data pipeline",
    schedule_interval="@daily",
    catchup=False,
)


# Data quality check task
def check_data_quality():
    print("Running data quality checks...")
    return True


check_quality = PythonOperator(
    task_id="check_data_quality",
    python_callable=check_data_quality,
    dag=etl_dag,
)

# Example extract task
extract_data = BashOperator(
    task_id="extract_data",
    bash_command='echo "Extracting data from CSV files"',
    dag=etl_dag,
)

# Example transform task
transform_data = BashOperator(
    task_id="transform_data",
    bash_command='echo "Transforming data"',
    dag=etl_dag,
)

# Example load task
load_data = BashOperator(
    task_id="load_data",
    bash_command='echo "Loading data to database"',
    dag=etl_dag,
)

# Task dependencies
extract_data >> transform_data >> load_data >> check_quality
