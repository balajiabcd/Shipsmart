# Milestone #174: Create Prompt Templates

**Your Role:** AI/LLM Engineer

Design LLM prompts for logistics:

```python
# src/llm/prompts.py

class PromptTemplates:
    @staticmethod
    def delay_explanation(prediction: dict) -> str:
        return f"""You are a logistics expert. Explain why a delivery might be delayed.
        
Prediction Details:
- Delay Probability: {prediction['delay_probability']:.1%}
- Risk Level: {prediction['risk_level']}
- Top Factors: {', '.join(prediction.get('top_factors', []))}

Provide a clear, concise explanation in 2-3 sentences that a customer service agent can understand."""

    @staticmethod
    def recommendation_explanation(recommendation: dict) -> str:
        return f"""Explain this logistics recommendation to a warehouse manager:

Action: {recommendation['action_type']}
Priority: {recommendation.get('priority', 'medium')}
Expected Impact: {recommendation.get('impact_score', 'moderate')}

Provide actionable advice in bullet points."""

    @staticmethod
    def delivery_summary(delivery_data: dict) -> str:
        return f"""Summarize this delivery status for a dashboard:

Delivery ID: {delivery_data['delivery_id']}
Status: {delivery_data['status']}
ETA: {delivery_data['eta']}
Issues: {delivery_data.get('issues', 'None')}

Provide a one-paragraph summary."""

    @staticmethod
    def customer_message(delivery_id: str, context: dict) -> str:
        tone = context.get('urgency', 'neutral')
        return f"""Generate a {tone} notification message for customer about delivery {delivery_id}.

Situation: {context.get('situation', 'standard delivery')}
Expected Delay: {context.get('delay_minutes', 0)} minutes

Keep it under 100 words, friendly and professional."""
```

Commit.