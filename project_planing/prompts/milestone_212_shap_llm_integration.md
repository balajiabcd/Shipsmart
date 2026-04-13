# Milestone #212: Combine SHAP with LLM

**Your Role:** AI/LLM Engineer

Integrate SHAP explanations with LLM:

```python
# src/root_cause/shap_llm_integration.py

import shap
import joblib
import numpy as np
import pandas as pd

class SHAPLLMIntegrator:
    def __init__(self, model, llm_client):
        self.model = model
        self.llm = llm_client
        self.explainer = shap.TreeExplainer(model)
    
    def explain_prediction(self, features: pd.DataFrame, delivery_context: dict) -> dict:
        # Get SHAP values
        shap_values = self.explainer.shap_values(features)
        
        # Convert to readable format
        feature_importance = self._format_shap_values(shap_values, features)
        
        # Generate natural language explanation
        nl_explanation = self._generate_nl_explanation(
            feature_importance, delivery_context
        )
        
        return {
            "prediction": float(self.model.predict_proba(features)[0][1]),
            "shap_values": feature_importance,
            "explanation": nl_explanation,
            "root_causes": self._extract_root_causes(feature_importance)
        }
    
    def _format_shap_values(self, shap_values, features):
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For binary: get delay class
        
        feature_names = features.columns.tolist() if hasattr(features, 'columns') else [f"f{i}" for i in range(len(features))]
        
        formatted = []
        for i, (name, value) in enumerate(zip(feature_names, shap_values[0])):
            formatted.append({
                "feature": name,
                "shap_value": float(value),
                "direction": "increases_delay" if value > 0 else "decreases_delay",
                "abs_value": float(abs(value))
            })
        
        return sorted(formatted, key=lambda x: x["abs_value"], reverse=True)
    
    def _generate_nl_explanation(self, shap_values, context):
        top_factors = [f"{s['feature']}: {s['direction']}" for s in shap_values[:3]]
        
        prompt = f"""Explain why a delivery has high delay probability.

Top contributing factors (SHAP values):
{chr(10).join(top_factors)}

Context:
- Weather: {context.get('weather', 'unknown')}
- Traffic: {context.get('traffic', 'unknown')}
- Distance: {context.get('distance', 'unknown')} km

Provide a 2-3 sentence explanation in plain language."""
        
        return self.llm.generate(prompt)
    
    def _extract_root_causes(self, shap_values, threshold: float = 0.1):
        return [
            s["feature"] for s in shap_values 
            if s["abs_value"] > threshold and s["shap_value"] > 0
        ]
```

Commit.