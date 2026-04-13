# Milestone #146: Create SHAP Waterfall Plots

**Your Role:** ML Engineer 2

Create waterfall plots for local explanations:

```python
import shap

shap_values = np.load('models/shap_values.npy')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

explainer = shap.TreeExplainer(best_model)

# Create waterfall plots for first 50 samples
for i in range(min(50, len(X_test))):
    plt.figure()
    shap.plots.waterfall(
        shap.Explanation(
            values=shap_values[i, :],
            base_values=explainer.expected_value,
            data=X_test.iloc[i, :],
            feature_names=X_test.columns.tolist()
        ),
        show=False
    )
    plt.savefig(f'models/waterfall_plots/waterfall_{i}.png', dpi=150, bbox_inches='tight')
    plt.close()

print("Saved 50 waterfall plots")
```

Save to `models/waterfall_plots/`. Commit.