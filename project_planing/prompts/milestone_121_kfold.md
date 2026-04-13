# Milestone #121: Cross-validation - K-fold

**Your Role:** ML Engineer 1

Perform standard K-fold cross-validation:
```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=42)
model = XGBClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=kf, scoring='f1')

print(f"K-fold F1: {scores.mean():.4f} (+/- {scores.std()*2:.4f})")
```

Log results. Commit.