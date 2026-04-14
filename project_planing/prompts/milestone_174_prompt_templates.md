# Milestone #174: Create Prompt Templates

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
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
```

**Completed:**
- Created `src/llm/prompts.py` with:
  - `PromptTemplates` class with various prompt generators:
    - `delay_explanation()` - Explain delays to agents
    - `recommendation_explanation()` - Explain recommendations
    - `delivery_summary()` - Dashboard summaries
    - `customer_message()` - Customer notifications
    - `root_cause_analysis()` - Root cause analysis
    - `operational_advice()` - Operations recommendations
    - System prompts for chat/explanation/recommendation
  - `get_template()` - Template retrieval
  - `format_prompt()` - Template formatting

**Next Milestone:** Proceed to #175 - Chat Interface

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #175: Create Chat Interface
- CLI-based chat with LLM
- Handle conversation context