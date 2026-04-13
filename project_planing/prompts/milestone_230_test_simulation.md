# Milestone #230: Test Simulation Accuracy

**Your Role:** AI/LLM Engineer

Validate simulation predictions:

```python
# tests/test_simulation.py

import pytest
import numpy as np
from src.simulation.framework import SimulationConfig
from src.simulation.demand_simulation import DemandSimulation
from src.simulation.weather_impact import WeatherImpactSimulation

@pytest.fixture
def base_config():
    return SimulationConfig(
        name="test",
        duration_hours=12,
        num_deliveries=50,
        num_drivers=10,
        num_warehouses=2,
        random_seed=42
    )

def test_demand_simulation_runs(base_config):
    sim = DemandSimulation(base_config, demand_multiplier=1.5)
    results = sim.run_simulation()
    
    assert "total_deliveries" in results
    assert results["total_deliveries"] == 75  # 50 * 1.5

def test_weather_impact_simulation(base_config):
    sim = WeatherImpactSimulation(base_config, "storm")
    results = sim.run_simulation()
    
    assert results["weather_scenario"] == "storm"
    assert "total_delay_minutes" in results
    assert results["total_delay_minutes"] > 0

def test_simulation_determinism():
    config = SimulationConfig(
        name="determinism_test",
        duration_hours=6,
        num_deliveries=20,
        num_drivers=5,
        num_warehouses=2,
        random_seed=123
    )
    
    sim1 = DemandSimulation(config, 1.0)
    results1 = sim1.run_simulation()
    
    sim2 = DemandSimulation(config, 1.0)
    results2 = sim2.run_simulation()
    
    assert results1["total_deliveries"] == results2["total_deliveries"]

def test_scenario_builder():
    from src.simulation.scenario_builder import ScenarioBuilder
    
    builder = ScenarioBuilder(base_config)
    scenario = builder.build_demand_scenario(2.0, "high_demand")
    
    assert scenario.num_deliveries == 100
```

Run:
```bash
pytest tests/test_simulation.py -v
```

Commit.