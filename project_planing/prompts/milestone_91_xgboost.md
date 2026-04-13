# Milestone #91: Train XGBoost (Classification)

**Your Role:** ML Engineer 1

Train XGBoost classifier:
```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)
```

Save to `models/xgboost_classifier.pkl`. Evaluate and log in MLflow. Commit.