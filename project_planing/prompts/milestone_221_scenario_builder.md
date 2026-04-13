# Milestone #221: Create What-If Scenario Builder

**Your Role:** AI/LLM Engineer

Define scenario inputs:

```python
# src/simulation/scenario_builder.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class ScenarioParameters:
    demand_multiplier: float = 1.0
    driver_availability: float = 1.0
    weather_severity: float = 0.0
    traffic_increase: float = 0.0
    fuel_price_change: float = 0.0
    warehouse_capacity_change: float = 0.0

class ScenarioBuilder:
    def __init__(self, base_config):
        self.base = base_config
        self.scenarios = {}
    
    def build_demand_scenario(self, multiplier: float, name: str = "demand_increase") -> SimulationConfig:
        return self._apply_params(
            name, 
            ScenarioParameters(demand_multiplier=multiplier)
        )
    
    def build_driver_shortage_scenario(self, availability: float, name: str = "driver_shortage") -> SimulationConfig:
        return self._apply_params(
            name,
            ScenarioParameters(driver_availability=availability)
        )
    
    def build_weather_scenario(self, severity: float, name: str = "severe_weather") -> SimulationConfig:
        return self._apply_params(
            name,
            ScenarioParameters(weather_severity=severity)
        )
    
    def build_traffic_scenario(self, increase: float, name: str = "high_traffic") -> SimulationConfig:
        return self._apply_params(
            name,
            ScenarioParameters(traffic_increase=increase)
        )
    
    def build_fuel_price_scenario(self, change: float, name: str = "fuel_price_increase") -> SimulationConfig:
        return self._apply_params(
            name,
            ScenarioParameters(fuel_price_change=change)
        )
    
    def build_warehouse_outage_scenario(self, warehouse_id: str, name: str = "warehouse_outage") -> dict:
        return {
            "name": name,
            "type": "outage",
            "affected_warehouse": warehouse_id,
            "description": f"Warehouse {warehouse_id} is offline"
        }
    
    def _apply_params(self, name: str, params: ScenarioParameters) -> SimulationConfig:
        config = self.base.copy()
        
        if params.demand_multiplier != 1.0:
            config.num_deliveries = int(config.num_deliveries * params.demand_multiplier)
        
        if params.driver_availability != 1.0:
            config.num_drivers = int(config.num_drivers * params.driver_availability)
        
        self.scenarios[name] = params
        return config
```

Commit.