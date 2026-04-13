# Milestone #132: Ensemble Models

**Your Role:** ML Engineers

Combine multiple models for better predictions:
```python
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier(
    estimators=[
        ('xgb', xgb_model),
        ('lgb', lgb_model),
        ('rf', rf_model)
    ],
    voting='soft'
)
ensemble.fit(X_train, y_train)
```

Create ensemble for both classification and regression. Save to `models/ensemble_classifier.pkl` and `models/ensemble_regressor.pkl`. Evaluate. Commit.