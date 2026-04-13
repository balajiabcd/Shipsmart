# Milestone #123: Cross-validation - TimeSeriesSplit

**Your Role:** ML Engineer 2

Use TimeSeriesSplit for temporal data (respecting time order):
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(model, X_train, y_train, cv=tscv, scoring='neg_mean_squared_error')
print(f"TimeSeriesSplit RMSE: {-scores.mean():.4f}")
```

Log results. Commit.