from typing import Dict, List, Any


class PromptTemplates:
    @staticmethod
    def delay_explanation(prediction: dict) -> str:
        return f"""You are a logistics expert. Explain why a delivery might be delayed.
        
Prediction Details:
- Delay Probability: {prediction["delay_probability"]:.1%}
- Risk Level: {prediction["risk_level"]}
- Top Factors: {", ".join(prediction.get("top_factors", []))}

Provide a clear, concise explanation in 2-3 sentences that a customer service agent can understand."""

    @staticmethod
    def recommendation_explanation(recommendation: dict) -> str:
        return f"""Explain this logistics recommendation to a warehouse manager:

Action: {recommendation["action_type"]}
Priority: {recommendation.get("priority", "medium")}
Expected Impact: {recommendation.get("impact_score", "moderate")}

Provide actionable advice in bullet points."""

    @staticmethod
    def delivery_summary(delivery_data: dict) -> str:
        return f"""Summarize this delivery status for a dashboard:

Delivery ID: {delivery_data["delivery_id"]}
Status: {delivery_data["status"]}
ETA: {delivery_data["eta"]}
Issues: {delivery_data.get("issues", "None")}

Provide a one-paragraph summary."""

    @staticmethod
    def customer_message(delivery_id: str, context: dict) -> str:
        tone = context.get("urgency", "neutral")
        return f"""Generate a {tone} notification message for customer about delivery {delivery_id}.

Situation: {context.get("situation", "standard delivery")}
Expected Delay: {context.get("delay_minutes", 0)} minutes

Keep it under 100 words, friendly and professional."""

    @staticmethod
    def root_cause_analysis(factors: List[Dict], context: Dict) -> str:
        return f"""Analyze the root causes of potential delivery delay.

Delay Factors:
"""
        for f in factors:
            f"- {f.get('feature')}: {f.get('impact')}"

        f"""
Context:
- Current weather: {context.get("weather", "unknown")}
- Traffic conditions: {context.get("traffic", "unknown")}
- Driver history: {context.get("driver_performance", "unknown")}

Identify the 3 most likely root causes and explain how they interact."""

    @staticmethod
    def operational_advice(context: Dict) -> str:
        return f"""You are a logistics operations advisor. Based on current conditions:

- Weather severity: {context.get("weather_severity", "N/A")}/10
- Traffic index: {context.get("traffic_index", "N/A")}/10  
- Active deliveries at risk: {context.get("deliveries_at_risk", "N/A")}
- Warehouse capacity: {context.get("warehouse_capacity", "N/A")}%

Provide 5 actionable operational recommendations. Keep each under 12 words."""

    @staticmethod
    def chat_system_prompt() -> str:
        return """You are ShipSmart's AI assistant for logistics operations. You help customer service agents, warehouse managers, and dispatchers with:
- Explaining delivery delays in simple terms
- Providing operational recommendations
- Answering questions about shipping policies
- Analyzing root causes of delivery issues

Be helpful, clear, and practical. When recommending actions, consider cost-benefit implications."""

    @staticmethod
    def explanation_system_prompt() -> str:
        return """You are a logistics expert explaining delivery delays to customer service representatives.
- Use simple, non-technical language
- Focus on actionable insights
- Be empathetic to customer concerns
- Keep explanations under 3 sentences"""

    @staticmethod
    def recommendation_system_prompt() -> str:
        return """You are a logistics operations assistant.
- Provide specific, actionable recommendations
- Consider operational costs and benefits
- Prioritize high-impact actions
- Keep recommendations concise"""


def get_template(template_name: str) -> str:
    """Get a specific prompt template"""
    templates = {
        "delay_explanation": PromptTemplates.delay_explanation,
        "recommendation_explanation": PromptTemplates.recommendation_explanation,
        "delivery_summary": PromptTemplates.delivery_summary,
        "customer_message": PromptTemplates.customer_message,
        "root_cause_analysis": PromptTemplates.root_cause_analysis,
        "operational_advice": PromptTemplates.operational_advice,
        "chat_system": PromptTemplates.chat_system_prompt,
        "explanation_system": PromptTemplates.explanation_system_prompt,
        "recommendation_system": PromptTemplates.recommendation_system_prompt,
    }
    return templates.get(template_name, "")


def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with variables"""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return template
