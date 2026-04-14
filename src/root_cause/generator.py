from typing import List, Dict
import asyncio


class NLExplanationGenerator:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def set_llm(self, llm_client):
        self.llm = llm_client

    async def generate_explanation(
        self, prediction_result: Dict, delivery_context: Dict
    ) -> Dict:
        prompt = self._build_explanation_prompt(prediction_result, delivery_context)

        if self.llm is not None:
            try:
                explanation = await self.llm.generate(prompt)
            except:
                explanation = self._fallback_explanation(
                    prediction_result, delivery_context
                )
        else:
            explanation = self._fallback_explanation(
                prediction_result, delivery_context
            )

        return self._format_explanation(explanation, prediction_result)

    def _build_explanation_prompt(self, prediction: Dict, context: Dict) -> str:
        shap_values = prediction.get("shap_values", [])[:5]

        shap_text = "\n".join(
            [
                f"- {s['feature']}: SHAP value {s.get('shap_value', 0):.3f} ({s.get('direction', 'unknown')})"
                for s in shap_values
            ]
        )

        return f"""Generate a clear, concise explanation of why a delivery is likely to be delayed.

SHAP Feature Importance (top 5):
{shap_text}

Delivery Context:
- Distance: {context.get("distance_km", "unknown")} km
- Weather: {context.get("weather_condition", "unknown")}
- Traffic Index: {context.get("traffic_index", "unknown")}
- Driver Performance: {context.get("driver_performance", "unknown")}%
- Time of Day: {context.get("time_of_day", "unknown")}

Requirements:
1. Start with the most important factor
2. Use simple language
3. Keep under 100 words
4. Include actionable insight if possible"""

    def _fallback_explanation(self, prediction: Dict, context: Dict) -> str:
        shap_values = prediction.get("shap_values", [])[:3]

        if not shap_values:
            return "The delay prediction is based on multiple factors. Review the detailed breakdown for more information."

        factors = []
        for s in shap_values:
            direction = "increases" if s.get("shap_value", 0) > 0 else "decreases"
            factors.append(f"{s['feature']} {direction} delay probability")

        return (
            f"Key factors: {', '.join(factors)}. "
            f"Current conditions show {context.get('weather_condition', 'unknown')} weather and "
            f"{context.get('traffic_index', 'unknown')} traffic conditions."
        )

    def _format_explanation(self, explanation: str, prediction: Dict) -> Dict:
        return {
            "explanation": explanation,
            "confidence": prediction.get("prediction", 0.5),
            "key_factors": [
                s["feature"] for s in prediction.get("shap_values", [])[:3]
            ],
            "formatted": self._markdown_format(explanation),
        }

    def _markdown_format(self, text: str) -> str:
        return f"> {text.replace('. ', '.  \n> ')}"


async def generate_batch_explanations(
    predictions: List[Dict], context: Dict, llm_client=None
) -> List[Dict]:
    generator = NLExplanationGenerator(llm_client)
    tasks = [generator.generate_explanation(pred, context) for pred in predictions]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    generator = NLExplanationGenerator()
    print("NL explanation generator ready")
