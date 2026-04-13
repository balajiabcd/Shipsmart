# Milestone #176: Integrate LLM with Predictions

**Your Role:** AI/LLM Engineer

Connect LLM with ML model outputs:

```python
# src/llm/prediction_integration.py

class PredictionIntegrator:
    def __init__(self, ml_model, llm_router, shap_explainer):
        self.ml_model = ml_model
        self.llm = llm_router
        self.shap = shap_explainer
    
    async def get_human_readable_prediction(self, delivery_context: dict) -> dict:
        # Get ML prediction
        features = self._extract_features(delivery_context)
        ml_prediction = self.ml_model.predict_proba([features])[0]
        
        # Get SHAP values for explanation
        shap_values = self.shap.shap_values([features])
        top_factors = self._get_top_shap_factors(shap_values, features)
        
        # Generate natural language explanation via LLM
        explanation_prompt = self._build_explanation_prompt(
            delay_prob=ml_prediction[1],
            top_factors=top_factors,
            context=delivery_context
        )
        
        llm_explanation = await self.llm.generate(explanation_prompt, complexity="medium")
        
        return {
            "prediction": {
                "on_time_probability": float(ml_prediction[0]),
                "delay_probability": float(ml_prediction[1]),
                "risk_level": self._classify_risk(ml_prediction[1])
            },
            "explanation": llm_explanation,
            "top_factors": top_factors,
            "recommendations": self._generate_recommendations(ml_prediction[1], top_factors)
        }
    
    def _build_explanation_prompt(self, delay_prob: float, top_factors: list, context: dict) -> str:
        return f"""A delivery has {delay_prob:.0%} probability of being delayed.
        
Top contributing factors:
{chr(10).join(f"- {f['feature']}: {f['impact']}" for f in top_factors[:5])}

Delivery context:
- Distance: {context.get('distance_km', 'unknown')} km
- Weather: {context.get('weather_condition', 'unknown')}
- Traffic: {context.get('traffic_level', 'unknown')}

Explain this in simple terms for a customer service representative. Keep under 3 sentences."""
    
    def _get_top_shap_factors(self, shap_values, features):
        feature_names = features.columns if hasattr(features, 'columns') else [f"feature_{i}" for i in range(len(features))]
        abs_shap = [abs(s) for s in shap_values[0]] if isinstance(shap_values, list) else [abs(s) for s in shap_values[0]]
        
        sorted_idx = sorted(range(len(abs_shap)), key=lambda i: abs_shap[i], reverse=True)
        
        return [
            {"feature": feature_names[i], "impact": "increases" if shap_values[0][i] > 0 else "decreases", "value": abs_shap[i]}
            for i in sorted_idx[:5]
        ]
    
    def _classify_risk(self, prob):
        if prob > 0.7: return "high"
        if prob > 0.4: return "medium"
        return "low"
    
    def _generate_recommendations(self, delay_prob, top_factors):
        if delay_prob < 0.3:
            return ["Continue normal operations"]
        
        recs = []
        if any(f['feature'] in ['weather', 'storm', 'rain'] for f in top_factors):
            recs.append("Consider rerouting to avoid severe weather")
        if any(f['feature'] in ['traffic', 'congestion'] for f in top_factors):
            reschedule to off-peak hours
        return recs if recs else ["Monitor closely"]
```

Commit.