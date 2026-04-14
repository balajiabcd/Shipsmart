# Milestone #152: Create Permutation Importance

**Status:** COMPLETED

**Your Role:** ML Engineer 2

**Instructions:**
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

**Completed:**
- Created `src/explainability/permutation_importance.py` with:
  - `calculate_permutation_importance()` - calculate importance
  - `save_permutation_importance()` / `load_permutation_importance()` - persistence
  - `plot_permutation_importance()` - visualization
  - `compare_permutation_shap()` - compare methods

**Next Milestone:** Proceed to #153 - Partial Dependence Plots

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #153: Create Partial Dependence Plots
- Use sklearn.inspection.partial_dependence
- Create visualizations for top features