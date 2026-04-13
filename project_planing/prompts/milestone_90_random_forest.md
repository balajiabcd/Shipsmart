# Milestone #90: Train Random Forest (Classification)

**Your Role:** ML Engineer 1

Train Random Forest classifier:
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
```

Save to `models/random_forest.pkl`. Evaluate: F1, ROC-AUC, precision, recall. Log in MLflow. Commit.