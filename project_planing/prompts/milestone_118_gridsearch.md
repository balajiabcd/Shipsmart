# Milestone #118: Hyperparameter Tuning - GridSearch

**Your Role:** ML Engineers

Use GridSearchCV to tune best models:
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, 15],
    'learning_rate': [0.05, 0.1, 0.2]
}

grid_search = GridSearchCV(
    XGBClassifier(),
    param_grid,
    cv=3,
    scoring='f1',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)
```

Save best params. Commit.