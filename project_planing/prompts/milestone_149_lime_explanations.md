# Milestone #149: Generate LIME Explanations

**Your Role:** ML Engineer 2

Generate LIME explanations for model predictions:

```python
import lime
import lime.lime_tabular
import pandas as pd
import joblib

# Load model and data
model = joblib.load('models/best_classifier.pkl')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

# Create LIME explainer
explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_test.values,
    feature_names=X_test.columns.tolist(),
    class_names=['OnTime', 'Delayed'],
    mode='classification'
)

# Generate explanations for first 100 samples
explanations = []
for i in range(min(100, len(X_test))):
    exp = explainer.explain_instance(
        X_test.iloc[i].values,
        model.predict_proba,
        num_features=10
    )
    explanations.append({
        'sample_id': i,
        'explanation': exp.as_list(),
        'prediction': model.predict([X_test.iloc[i].values])[0]
    })

# Save explanations
import json
with open('models/lime_explanations.json', 'w') as f:
    json.dump(explanations, f, indent=2)

print(f"Generated {len(explanations)} LIME explanations")
```

Commit the code.