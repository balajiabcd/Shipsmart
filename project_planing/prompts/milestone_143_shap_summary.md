# Milestone #143: Create SHAP Summary Plots

**Your Role:** ML Engineer 2

Create summary plot:
```python
import shap
import matplotlib.pyplot as plt

shap_values = np.load('models/shap_values.npy')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig('models/shap_summary.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved shap_summary.png")
```

Save to `models/shap_summary.png`. Commit.