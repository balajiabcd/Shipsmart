import shap
import xgboost
from sklearn.datasets import make_classification

print(f"SHAP version: {shap.__version__}")

X, y = make_classification(n_samples=100, n_features=5, random_state=42)
model = xgboost.XGBClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X[:5])

print("SHAP installed successfully!")
print(f"SHAP values shape: {shap_values.shape}")
