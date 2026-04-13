# Milestone #122: Cross-validation - Stratified

**Your Role:** ML Engineer 1

Perform Stratified K-fold to maintain class distribution:
```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='f1')
print(f"Stratified K-fold F1: {scores.mean():.4f}")
```

Log results. Commit.