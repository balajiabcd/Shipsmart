# Milestone #145: Create SHAP Force Plots

**Your Role:** ML Engineer 2

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

Save to `models/force_plots/`. Commit.