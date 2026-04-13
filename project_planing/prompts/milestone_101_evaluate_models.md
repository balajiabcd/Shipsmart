# Milestone #101: Evaluate All Classification Models

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #100 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Calculate F1, ROC-AUC, Precision, Recall for All Models

**Your Role:** ML Engineer 1

**Instructions:**
1. Create `src/ml_models/evaluate_models.py`:
   ```python
   import pandas as pd
   import joblib
   from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
   
   models = [
       'logistic_regression', 'random_forest', 'xgboost',
       'lightgbm', 'catboost', 'svm', 'naive_bayes', 'knn',
       'decision_tree', 'adaboost', 'gradient_boosting', 'extra_trees'
   ]
   
   X_val = pd.read_csv('data/ml/val_features.csv').fillna(0)
   y_val = pd.read_csv('data/ml/val_target_class.csv')['is_delayed']
   
   results = []
   for name in models:
       model = joblib.load(f'models/{name}.pkl')
       if name == 'svm' or name == 'knn':
           from sklearn.preprocessing import StandardScaler
           scaler = joblib.load('models/logistic_regression_scaler.pkl')
           X_val_scaled = scaler.transform(X_val)
           y_pred = model.predict(X_val_scaled)
           y_proba = model.predict_proba(X_val_scaled)[:, 1]
       else:
           y_pred = model.predict(X_val)
           y_proba = model.predict_proba(X_val)[:, 1]
       
       results.append({
           'model': name,
           'f1': f1_score(y_val, y_pred),
           'roc_auc': roc_auc_score(y_val, y_proba),
           'precision': precision_score(y_val, y_pred),
           'recall': recall_score(y_val, y_pred)
       })
   
   results_df = pd.DataFrame(results).sort_values('f1', ascending=False)
   results_df.to_csv('data/ml/classification_results.csv', index=False)
   print(results_df)
   ```

2. Run evaluation
3. Save results
4. Identify best model

---

## Section 3: Instructions for Next AI Agent

*(Empty)*