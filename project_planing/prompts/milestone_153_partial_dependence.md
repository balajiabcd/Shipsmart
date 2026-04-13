# Milestone #153: Create Partial Dependence Plots

**Your Role:** ML Engineer 2

Create partial dependence plots (PDP):

```python
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay

model = joblib.load('models/best_classifier.pkl')
X = pd.read_csv('data/ml/test_features.csv').fillna(0)

# Get top features from importance
importance = pd.read_csv('models/feature_importance.csv')
top_features = importance['feature'].head(8).tolist()
feature_indices = [list(X.columns).index(f) for f in top_features]

# Create PDP for top 8 features
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
display = PartialDependenceDisplay.from_estimator(
    model, X, feature_indices, 
    ax=axes, n_jobs=-1
)
plt.tight_layout()
plt.savefig('models/pdp/plots.png', dpi=150)
plt.close()

# Also create individual PDPs
for i, feature in enumerate(top_features):
    plt.figure(figsize=(10, 6))
    PartialDependenceDisplay.from_estimator(
        model, X, [feature], 
        kind='both', subsample=1000
    )
    plt.savefig(f'models/pdp/{feature}_pdp.png', dpi=150)
    plt.close()

print("Saved partial dependence plots")
```

Save to `models/pdp/`. Commit.