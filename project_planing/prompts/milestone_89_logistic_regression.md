# Milestone #89: Train Logistic Regression (Classification)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #88 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Build Baseline Logistic Regression Model

**Your Role:** ML Engineer 1

**Instructions:**
1. Create `src/ml_models/logistic_regression.py`:
   ```python
   import pandas as pd
   from sklearn.linear_model import LogisticRegression
   from sklearn.preprocessing import StandardScaler
   from sklearn.metrics import f1_score, roc_auc_score, classification_report
   import joblib
   
   def train_logistic_regression():
       # Load data
       X_train = pd.read_csv('data/ml/train_features.csv')
       X_val = pd.read_csv('data/ml/val_features.csv')
       y_train = pd.read_csv('data/ml/train_target_class.csv')['is_delayed']
       y_val = pd.read_csv('data/ml/val_target_class.csv')['is_delayed']
       
       # Handle missing values
       X_train = X_train.fillna(0)
       X_val = X_val.fillna(0)
       
       # Scale features
       scaler = StandardScaler()
       X_train_scaled = scaler.fit_transform(X_train)
       X_val_scaled = scaler.transform(X_val)
       
       # Train model
       model = LogisticRegression(max_iter=1000, random_state=42)
       model.fit(X_train_scaled, y_train)
       
       # Predict
       y_pred = model.predict(X_val_scaled)
       y_pred_proba = model.predict_proba(X_val_scaled)[:, 1]
       
       # Evaluate
       print("Logistic Regression Results:")
       print(f"F1 Score: {f1_score(y_val, y_pred):.4f}")
       print(f"ROC-AUC: {roc_auc_score(y_val, y_pred_proba):.4f}")
       print(classification_report(y_val, y_pred))
       
       # Save model
       joblib.dump(model, 'models/logistic_regression.pkl')
       joblib.dump(scaler, 'models/logistic_regression_scaler.pkl')
       print("Model saved to models/logistic_regression.pkl")
   
   train_logistic_regression()
   ```

2. Run and evaluate
3. Save model to `models/` directory
4. Log results in MLflow
5. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*