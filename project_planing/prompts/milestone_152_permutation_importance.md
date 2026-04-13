# Milestone #152: Create Permutation Importance

**Your Role:** ML Engineer 2

Calculate permutation importance:

```python
import pandas as pd
import numpy as np
import joblib
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# Load model and data
model = joblib.load('models/best_classifier.pkl')
X = pd.read_csv('data/ml/train_features.csv').fillna(0)
y = pd.read_csv('data/ml/train_labels.csv')['delay_label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Calculate permutation importance
result = permutation_importance(
    model, X_test, y_test, 
    n_repeats=10, 
    random_state=42,
    n_jobs=-1
)

# Save results
importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance_mean': result.importances_mean,
    'importance_std': result.importances_std
}).sort_values('importance_mean', ascending=False)

importance_df.to_csv('models/permutation_importance.csv', index=False)
print("Top 10 features by permutation importance:")
print(importance_df.head(10))
```

Commit.