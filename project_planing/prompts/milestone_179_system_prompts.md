# Milestone #179: Add System Prompts

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
Define AI assistant behavior:

```python
# src/llm/system_prompts.py

SYSTEM_PROMPTS = {
    "default": """You are Shipsmart AI Assistant...""",
    "customer_service": """You are Shipsmart Customer Service AI...""",
    "warehouse_manager": """You are Shipsmart Warehouse Operations AI...""",
}
```

**Completed:**
- Created `src/llm/system_prompts.py` with:
  - `SYSTEM_PROMPTS` - Dictionary of role-based prompts
  - `get_system_prompt()` - Get prompt for role
  - `customize_prompt()` - Add custom instructions
  - `get_prompt_with_context()` - Include context
  - `list_available_roles()` - List all roles

**Next Milestone:** Proceed to #180 - Test LLM Integration

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #180: Test LLM Integration
- Test chat and prediction features