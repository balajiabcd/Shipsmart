# Milestone #144: Create SHAP Dependence Plots

**Your Role:** ML Engineer 2

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

Save to `models/shap_dependence_*.png`. Commit.