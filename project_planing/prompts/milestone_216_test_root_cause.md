# Milestone #216: Test Root Cause Outputs

**Your Role:** AI/LLM Engineer

Validate explanation quality:

```python
# tests/test_root_cause.py

import pytest
from src.root_cause.generator import NLExplanationGenerator

@pytest.fixture
def generator():
    return NLExplanationGenerator(llm_client)

@pytest.fixture
def sample_prediction():
    return {
        "prediction": 0.78,
        "shap_values": [
            {"feature": "weather_severity", "shap_value": 0.45, "direction": "increases_delay"},
            {"feature": "traffic_index", "shap_value": 0.32, "direction": "increases_delay"},
            {"feature": "distance_km", "shap_value": 0.15, "direction": "increases_delay"},
            {"feature": "driver_performance", "shap_value": -0.12, "direction": "decreases_delay"}
        ]
    }

@pytest.fixture
def sample_context():
    return {
        "distance_km": 45,
        "weather_condition": "heavy_rain",
        "traffic_index": 7,
        "driver_performance": 85
    }

@pytest.mark.asyncio
async def test_explanation_generation(generator, sample_prediction, sample_context):
    result = await generator.generate_explanation(sample_prediction, sample_context)
    
    assert result is not None
    assert len(result["explanation"]) > 0
    assert len(result["explanation"]) < 200  # Within word limit
    assert "weather" in result["explanation"].lower() or "rain" in result["explanation"].lower()

def test_root_cause_extraction(sample_prediction):
    from src.root_cause.shap_llm_integration import SHAPLLMIntegrator
    
    causes = SHAPLLMIntegrator._extract_root_causes(
        sample_prediction["shap_values"], threshold=0.1
    )
    
    assert "weather_severity" in causes
    assert "traffic_index" in causes
    assert "driver_performance" not in causes  # Negative contribution

@pytest.mark.asyncio
async def test_batch_explanations():
    from src.root_cause.generator import generate_batch_explanations
    
    predictions = [{"shap_values": []}] * 5
    results = await generate_batch_explanations(predictions, {})
    
    assert len(results) == 5
```

Run:
```bash
pytest tests/test_root_cause.py -v
```

Commit.