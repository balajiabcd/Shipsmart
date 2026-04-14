import pytest
import asyncio
from src.root_cause.generator import NLExplanationGenerator
from src.root_cause.shap_llm_integration import SHAPLLMIntegrator
from src.root_cause.confidence import ConfidenceScorer


@pytest.fixture
def generator():
    return NLExplanationGenerator()


@pytest.fixture
def sample_prediction():
    return {
        "prediction": 0.78,
        "shap_values": [
            {
                "feature": "weather_severity",
                "shap_value": 0.45,
                "direction": "increases_delay",
            },
            {
                "feature": "traffic_index",
                "shap_value": 0.32,
                "direction": "increases_delay",
            },
            {
                "feature": "distance_km",
                "shap_value": 0.15,
                "direction": "increases_delay",
            },
            {
                "feature": "driver_performance",
                "shap_value": -0.12,
                "direction": "decreases_delay",
            },
        ],
    }


@pytest.fixture
def sample_context():
    return {
        "distance_km": 45,
        "weather_condition": "heavy_rain",
        "traffic_index": 7,
        "driver_performance": 85,
    }


@pytest.mark.asyncio
async def test_explanation_generation(generator, sample_prediction, sample_context):
    result = await generator.generate_explanation(sample_prediction, sample_context)

    assert result is not None
    assert "explanation" in result
    assert len(result["explanation"]) > 0
    assert "key_factors" in result


def test_root_cause_extraction(sample_prediction):
    integrator = SHAPLLMIntegrator()

    causes = integrator._extract_root_causes(
        sample_prediction["shap_values"], threshold=0.1
    )

    assert "weather_severity" in causes
    assert "traffic_index" in causes
    assert "driver_performance" not in causes


def test_confidence_scorer(sample_prediction):
    scorer = ConfidenceScorer()

    result = scorer.calculate_confidence(
        prediction=sample_prediction["prediction"],
        shap_values=sample_prediction["shap_values"],
        feature_values={"weather": "rain", "traffic": "high"},
    )

    assert "overall" in result
    assert "rating" in result
    assert result["rating"] in ["very_high", "high", "medium", "low", "very_low"]


@pytest.mark.asyncio
async def test_batch_explanations():
    predictions = [{"shap_values": [{"feature": "test", "shap_value": 0.1}]}] * 3
    results = await asyncio.gather(
        *[
            generator.generate_explanation(pred, {})
            for generator, pred in [(NLExplanationGenerator(), p) for p in predictions]
        ]
    )

    assert len(results) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
