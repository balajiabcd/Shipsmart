# Milestone #151: Integrate SHAP with API

**Status:** COMPLETED

**Your Role:** ML Engineer 2

**Instructions:**
Add SHAP explanation endpoint to API:

```python
# In api/endpoints/explainability.py
from fastapi import APIRouter
import shap
import joblib
import pandas as pd
import numpy as np

router = APIRouter(prefix="/explain", tags=["Explainability"])

model = joblib.load('models/best_classifier.pkl')
explainer = shap.TreeExplainer(model)

@router.post("/shap")
async def explain_with_shap(features: dict):
    """Return SHAP values for a single prediction"""
    df = pd.DataFrame([features])
    shap_values = explainer.shap_values(df)
    
    return {
        "shap_values": shap_values[0].tolist() if isinstance(shap_values, list) else shap_values.tolist(),
        "base_value": float(explainer.expected_value),
        "prediction": int(model.predict(df)[0])
    }

@router.get("/feature-importance")
async def get_feature_importance():
    """Return global feature importance"""
    importance = pd.read_csv('models/feature_importance.csv')
    return importance.to_dict(orient="records")
```

**Completed:**
- Created `src/api/endpoints/explainability.py` with endpoints:
  - `POST /explain/shap` - single prediction SHAP explanation
  - `GET /explain/feature-importance` - global feature importance
  - `POST /explain/shap-batch` - batch SHAP explanations
  - `GET /explain/model-info` - model information

**Next Milestone:** Proceed to #152 - Permutation Importance

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #152: Calculate Permutation Importance
- Use sklearn.inspection.permutation_importance
- Compare with SHAP importance