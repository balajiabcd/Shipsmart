# Milestone #142: Generate SHAP Values for Best Model

**Your Role:** ML Engineer 2

Generate SHAP values:
```python
import shap
import joblib

model = joblib.load('models/best_classifier.pkl')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Save SHAP values
np.save('models/shap_values.npy', shap_values)
print(f"SHAP values shape: {shap_values.shape}")
```

Save to `models/shap_values.npy`. Commit.