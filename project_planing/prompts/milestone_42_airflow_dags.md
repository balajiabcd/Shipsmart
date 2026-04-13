# Milestone #42: Set Up Airflow DAGs

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #41 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Configure Apache Airflow

**Your Role:** DevOps Engineer

**Instructions:**
1. Create docker-compose for Airflow:
   ```yaml
   # docker/airflow/docker-compose.yml
   services:
     postgres:
       image: postgres:13
       environment:
         POSTGRES_DB: airflow
         POSTGRES_USER: airflow
         POSTGRES_PASSWORD: airflow
     
     redis:
       image: redis:7
       
     airflow-webserver:
       image: apache/airflow:2.7.1
       depends_on: [postgres, redis]
       environment:
         AIRFLOW__CORE__EXECUTOR: CeleryExecutor
         AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
         AIRFLOW__CELERY__RESULT_BACKEND: redis://redis:6379/0
       volumes:
         - ./dags:/opt/airflow/dags
   ```

2. Create DAGs folder structure in `dags/`
3. Create basic DAG config `dags/airflow_config.py`
4. Commit and push

---

## Section 3: Instructions for Next AI Agent

*(Empty)*

### Milestone #42 Completed
- docker/airflow/docker-compose.yml (Airflow setup)
- dags/shipsmart_etl.py (main ETL DAG)
- Next: Milestone #43