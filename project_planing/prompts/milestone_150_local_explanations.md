# Milestone #150: Create Local Explanations

**Your Role:** ML Engineer 2

Create local explanation visualizations:

```python
import lime
import lime.lime_tabular
import matplotlib.pyplot as plt
import pandas as pd
import joblib

model = joblib.load('models/best_classifier.pkl')
X_test = pd.read_csv('data/ml/test_features.csv').fillna(0)

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_test.values,
    feature_names=X_test.columns.tolist(),
    class_names=['OnTime', 'Delayed'],
    mode='classification'
)

for i in range(min(30, len(X_test))):
    exp = explainer.explain_instance(
        X_test.iloc[i].values,
        model.predict_proba,
        num_features=10
    )
    fig = exp.as_pyplot_figure()
    fig.savefig(f'models/lime_plots/explanation_{i}.png', dpi=150, bbox_inches='tight')
    plt.close()

print("Saved 30 local explanation plots")
```

Save to `models/lime_plots/`. Commit.