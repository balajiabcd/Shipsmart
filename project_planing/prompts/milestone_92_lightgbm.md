# Milestone #92: Train LightGBM (Classification)

**Your Role:** ML Engineer 1

Train LightGBM classifier:
```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)
model.fit(X_train, y_train)
```

Save to `models/lightgbm_classifier.pkl`. Evaluate and log in MLflow. Commit.