# Milestone #119: Hyperparameter Tuning - RandomSearch

**Your Role:** ML Engineers

Use RandomSearchCV for efficient hyperparameter search:
```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [3, 5, 7, 10, 15],
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
    'subsample': [0.6, 0.8, 1.0]
}

random_search = RandomizedSearchCV(
    XGBClassifier(),
    param_dist,
    n_iter=50,
    cv=3,
    scoring='f1',
    random_state=42,
    n_jobs=-1
)
random_search.fit(X_train, y_train)
```

Save best params. Commit.