# Milestone #161: Integrate ML with Decision Rules

**Your Role:** AI/LLM Engineer

Combine ML predictions with rule-based logic:

```python
# decision_engine/hybrid_engine.py

class HybridDecisionEngine:
    def __init__(self, ml_model, rules_config):
        self.ml_model = ml_model
        self.rules = rules_config
        self.rule_evaluator = RuleEvaluator(rules_config)
    
    def make_decision(self, delivery_context: dict) -> dict:
        ml_prediction = self.ml_model.predict_proba(delivery_context)
        
        delivery_context["delay_probability"] = ml_prediction[1]
        
        triggered_rules = self.rule_evaluator.evaluate(delivery_context)
        
        recommendations = self._generate_recommendations(
            ml_prediction, triggered_rules, delivery_context
        )
        
        return {
            "prediction": ml_prediction,
            "risk_level": self._classify_risk(ml_prediction[1]),
            "recommendations": recommendations,
            "should_intervene": ml_prediction[1] > 0.5 or len(triggered_rules) > 0
        }
    
    def _generate_recommendations(self, ml_pred, rules, context):
        recs = []
        
        if ml_pred[1] > 0.7:
            recs.extend(self._high_risk_recommendations(context))
        
        for rule in rules:
            recs.append(self._rule_to_recommendation(rule, context))
        
        return rank_recommendations(recs, context)
    
    def _classify_risk(self, prob):
        if prob > 0.7: return "high"
        if prob > 0.4: return "medium"
        return "low"
```

Save to `src/decision_engine/hybrid_engine.py`. Commit.