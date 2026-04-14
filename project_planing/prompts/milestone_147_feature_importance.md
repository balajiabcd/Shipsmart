# Milestone #147: Generate Feature Importance Ranking

**Status:** COMPLETED

**Your Role:** ML Engineer 2

**Instructions:**
Generate and save feature importance ranking:

```python
import pandas as pd
import numpy as np
import shap

shap_values = np.load('models/shap_values.npy')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

# Calculate mean absolute SHAP values
feature_importance = pd.DataFrame({
    'feature': X_test.columns,
    'importance': np.abs(shap_values).mean(axis=0)
}).sort_values('importance', ascending=False)

feature_importance.to_csv('models/feature_importance.csv', index=False)

print("Top 10 Features:")
print(feature_importance.head(10))

# Also save as JSON for API
feature_importance.head(20).to_json('models/feature_importance.json', orient='records', indent=2)
```

**Completed:**
- Created `src/explainability/feature_importance.py` with:
  - `generate_shap_feature_importance()` - SHAP-based importance
  - `generate_model_feature_importance()` - model built-in importance
  - `compare_feature_importance()` - compare both methods
  - `plot_feature_importance_comparison()` - visualization
  - `save_feature_importance()` - save to CSV/JSON

**Next Milestone:** Proceed to #148 - Install LIME

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #148: Install LIME for Local Interpretability
- pip install lime
- Test basic import