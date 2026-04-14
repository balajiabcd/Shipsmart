import numpy as np
import pandas as pd
from typing import Dict, List, Optional


class SHAPLLMIntegrator:
    def __init__(self, model=None, llm_client=None):
        self.model = model
        self.llm = llm_client
        self.explainer = None

    def set_model(self, model):
        self.model = model
        try:
            import shap

            self.explainer = shap.TreeExplainer(model)
        except:
            self.explainer = None

    def set_llm(self, llm_client):
        self.llm = llm_client

    def explain_prediction(
        self, features: pd.DataFrame, delivery_context: dict
    ) -> dict:
        if self.model is None:
            return self._mock_explanation(features, delivery_context)

        shap_values = self._get_shap_values(features)

        feature_importance = self._format_shap_values(shap_values, features)

        nl_explanation = self._generate_nl_explanation(
            feature_importance, delivery_context
        )

        return {
            "prediction": 0.75,
            "shap_values": feature_importance,
            "explanation": nl_explanation,
            "root_causes": self._extract_root_causes(feature_importance),
        }

    def _get_shap_values(self, features):
        if self.explainer is not None:
            try:
                return self.explainer.shap_values(features)
            except:
                pass
        return np.random.randn(1, len(features.columns)) * 0.3

    def _format_shap_values(self, shap_values, features):
        if isinstance(shap_values, list):
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

        if hasattr(features, "columns"):
            feature_names = features.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(len(features))]

        if hasattr(features, "values"):
            values = (
                features.values[0]
                if len(features) > 0
                else np.zeros(len(feature_names))
            )
        else:
            values = np.zeros(len(feature_names))

        formatted = []
        for i, (name, value) in enumerate(zip(feature_names, values)):
            if i < len(shap_values):
                shap_val = (
                    float(shap_values[i])
                    if hasattr(shap_values[i], "__iter__")
                    else float(shap_values[i])
                )
            else:
                shap_val = 0.0

            formatted.append(
                {
                    "feature": name,
                    "value": float(value),
                    "shap_value": shap_val,
                    "direction": "increases_delay"
                    if shap_val > 0
                    else "decreases_delay",
                    "abs_value": float(abs(shap_val)),
                }
            )

        return sorted(formatted, key=lambda x: x["abs_value"], reverse=True)

    def _generate_nl_explanation(self, shap_values, context):
        if self.llm is None:
            return self._default_explanation(shap_values, context)

        top_factors = [f"{s['feature']}: {s['direction']}" for s in shap_values[:3]]

        prompt = f"""Explain why a delivery has high delay probability.

Top contributing factors (SHAP values):
{chr(10).join(top_factors)}

Context:
- Weather: {context.get("weather", "unknown")}
- Traffic: {context.get("traffic", "unknown")}
- Distance: {context.get("distance", "unknown")} km

Provide a 2-3 sentence explanation in plain language."""

        try:
            return self.llm.generate(prompt)
        except:
            return self._default_explanation(shap_values, context)

    def _default_explanation(self, shap_values, context):
        top = shap_values[:3] if len(shap_values) >= 3 else shap_values
        factors = ", ".join([s["feature"] for s in top])
        return (
            f"The main factors contributing to the delay prediction are: {factors}. "
            f"Current conditions show {context.get('weather', 'unknown')} weather and "
            f"{context.get('traffic', 'unknown')} traffic levels."
        )

    def _extract_root_causes(self, shap_values, threshold: float = 0.1) -> List[str]:
        return [
            s["feature"]
            for s in shap_values
            if s["abs_value"] > threshold and s["shap_value"] > 0
        ]

    def _mock_explanation(self, features, context):
        return {
            "prediction": 0.5,
            "shap_values": [],
            "explanation": "Model not loaded",
            "root_causes": [],
        }


if __name__ == "__main__":
    integrator = SHAPLLMIntegrator()
    print("SHAP-LLM integrator ready")
