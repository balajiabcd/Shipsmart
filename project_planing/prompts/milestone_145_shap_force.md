# Milestone #145: Create SHAP Force Plots

**Status:** COMPLETED

**Your Role:** ML Engineer 2

**Instructions:**
Create individual force plots:
```python
import shap

shap_values = np.load('models/shap_values.npy')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

# Create force plot for first 100 samples
for i in range(min(100, len(X_test))):
    shap.force_plot(
        explainer.expected_value,
        shap_values[i, :],
        X_test.iloc[i, :],
        matplotlib=True,
        show=False
    ).savefig(f'models/force_plots/force_{i}.png')

print("Saved 100 force plots")
```

**Completed:**
- Created `src/explainability/shap_force.py` with:
  - `create_shap_force_plot()` - single sample force plot
  - `create_force_plot_html()` - interactive HTML force plot
  - `create_batch_force_plots()` - batch generation of force plots
- Creates force_plots directory automatically

**Next Milestone:** Proceed to #146 - SHAP Waterfall Plot

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #146: Create SHAP Waterfall Plot
- Create waterfall plot for individual predictions
- Save to models/