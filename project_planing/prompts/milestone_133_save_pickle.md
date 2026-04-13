# Milestone #133: Save Trained Models (pickle)

**Your Role:** ML Engineer 1

Save all trained models as pickle files:
```python
import joblib

models = ['logistic_regression', 'random_forest', 'xgboost', 'lightgbm', 'catboost']
for name in models:
    joblib.dump(model, f'models/{name}.pkl')
    print(f"Saved {name}.pkl")
```

Ensure all sklearn models are saved. Verify all files exist. Commit.