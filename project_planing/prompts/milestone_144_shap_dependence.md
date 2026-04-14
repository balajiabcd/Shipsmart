# Milestone #144: Create SHAP Dependence Plots

**Status:** COMPLETED

**Your Role:** ML Engineer 2

**Instructions:**
Create dependence plots for top features:
```python
import shap
import matplotlib.pyplot as plt

shap_values = np.load('models/shap_values.npy')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

# Get feature importances
feature_importance = np.abs(shap_values).mean(axis=0)
top_features = X_test.columns[np.argsort(feature_importance)[-5:]]

for feature in top_features:
    plt.figure(figsize=(8, 6))
    shap.dependence_plot(feature, shap_values, X_test, show=False)
    plt.savefig(f'models/shap_dependence_{feature}.png', dpi=150, bbox_inches='tight')
    plt.close()

print("Saved dependence plots for top 5 features")
```

**Completed:**
- Created `src/explainability/shap_dependence.py` with:
  - `create_shap_dependence_plot()` - single dependence plot
  - `create_all_dependence_plots()` - creates plots for top N features
  - `get_top_features()` - extracts top features by importance
- Auto interaction index for feature interactions

**Next Milestone:** Proceed to #145 - SHAP Force Plot

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #145: Create SHAP Force Plot
- Create force plot for individual predictions
- Save as HTML for interactivity