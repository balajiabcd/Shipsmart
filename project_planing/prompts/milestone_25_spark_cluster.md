# Milestone #25: Set up Apache Spark Cluster

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #24 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Set up Apache Spark Cluster for Data Processing

**Your Role:** DevOps Engineer

**Instructions:**
1. Install Apache Spark:
   ```bash
   # Download Spark
   wget https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
   tar -xzf spark-3.4.1-bin-hadoop3.tgz
   
   # Set environment variables
   export SPARK_HOME=/path/to/spark-3.4.1-bin-hadoop3
   export PATH=$PATH:$SPARK_HOME/bin
   ```

2. Create Spark configuration in `config/spark/`
   - `spark-defaults.conf`
   - `log4j.properties`

3. Create docker-compose for Spark cluster:
   ```yaml
   # docker-compose.yml
   version: '3.8'
   services:
     spark-master:
       image: bitnami/spark:3.4.1
       ports:
         - "8080:8080"
         - "7077:7077"
     spark-worker-1:
       image: bitnami/spark:3.4.1
       environment:
         SPARK_MODE: worker
         SPARK_MASTER_URL: spark://spark-master:7077
   ```

4. Create startup script `scripts/start_spark.sh`
5. Commit and push

**Subagent Task:** None needed

---

## Section 3: Instructions for Next AI Agent

### Milestone #25 Completed
- config/spark/spark-defaults.conf
- docker/spark-compose.yml (master + 2 workers)
- scripts/start_spark.sh
- Next: Milestone #26