# Milestone #116: Evaluate All Regression Models

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #115 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Calculate RMSE, MAE, R² for All Regression Models

**Your Role:** ML Engineer 2

**Instructions:**
1. Evaluate all regression models:
   ```python
   from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
   
   models = ['linear_regression_reg', 'ridge_regression', 'lasso_regression',
             'elasticnet', 'random_forest_reg', 'xgboost_regressor', 
             'lightgbm_regressor', 'catboost_regressor', 'svr', 
             'knn_regressor', 'decision_tree_reg', 'gb_regressor', 'extra_trees_reg']
   
   results = []
   for name in models:
       model = joblib.load(f'models/{name}.pkl')
       y_pred = model.predict(X_val)
       results.append({
           'model': name,
           'rmse': np.sqrt(mean_squared_error(y_val_reg, y_pred)),
           'mae': mean_absolute_error(y_val_reg, y_pred),
           'r2': r2_score(y_val_reg, y_pred)
       })
   
   results_df = pd.DataFrame(results).sort_values('rmse')
   results_df.to_csv('data/ml/regression_results.csv', index=False)
   print(results_df)
   ```

2. Save results to `data/ml/regression_results.csv`

---

## Section 3: Instructions for Next AI Agent

*(Empty)*