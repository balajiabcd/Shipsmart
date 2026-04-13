# Milestone #120: Hyperparameter Tuning - Optuna

**Your Role:** ML Engineers

Use Optuna for Bayesian optimization:
```python
import optuna
from sklearn.model_selection import cross_val_score

def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 3, 15)
    learning_rate = trial.suggest_float('learning_rate', 0.01, 0.3)
    
    model = XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        random_state=42
    )
    
    score = cross_val_score(model, X_train, y_train, cv=3, scoring='f1')
    return score.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(f"Best params: {study.best_params}")
print(f"Best F1: {study.best_value}")
```

Save best params and retrain. Commit.