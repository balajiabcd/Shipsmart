# Milestone #135: Set Up MLflow Tracking

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #134 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Configure MLflow for Model Versioning

**Your Role:** DevOps Engineer

**Instructions:**
1. Install MLflow:
   ```bash
   pip install mlflow
   ```

2. Start MLflow server:
   ```bash
   mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow_artifacts
   ```

3. Configure tracking in code:
   ```python
   import mlflow
   mlflow.set_tracking_uri("http://localhost:5000")
   mlflow.set_experiment("shipsmart")
   
   with mlflow.start_run():
       mlflow.log_param("n_estimators", 100)
       mlflow.log_metric("f1_score", 0.85)
       mlflow.sklearn.log_model(model, "model")
   ```

4. Create MLflow UI dashboard
5. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty - To be filled by this agent after completion)*