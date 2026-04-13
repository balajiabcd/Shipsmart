# Milestone #93: Train CatBoost (Classification)

**Your Role:** ML Engineer 1

Train CatBoost classifier:
```python
from catboost import CatBoostClassifier

model = CatBoostClassifier(
    iterations=100,
    depth=6,
    learning_rate=0.1,
    random_state=42,
    verbose=0
)
model.fit(X_train, y_train)
```

Save to `models/catboost_classifier.pkl`. Evaluate and log in MLflow. Commit.