from dataclasses import dataclass
from typing import Dict, Optional
import copy


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
        self.scenarios: Dict = {}

    def build_demand_scenario(
        self, multiplier: float, name: str = "demand_increase"
    ) -> "SimulationConfig":
        return self._apply_params(
            name, ScenarioParameters(demand_multiplier=multiplier)
        )

    def build_driver_shortage_scenario(
        self, availability: float, name: str = "driver_shortage"
    ) -> "SimulationConfig":
        return self._apply_params(
            name, ScenarioParameters(driver_availability=availability)
        )

    def build_weather_scenario(
        self, severity: float, name: str = "severe_weather"
    ) -> "SimulationConfig":
        return self._apply_params(name, ScenarioParameters(weather_severity=severity))

    def build_traffic_scenario(
        self, increase: float, name: str = "high_traffic"
    ) -> "SimulationConfig":
        return self._apply_params(name, ScenarioParameters(traffic_increase=increase))

    def build_fuel_price_scenario(
        self, change: float, name: str = "fuel_price_increase"
    ) -> "SimulationConfig":
        return self._apply_params(name, ScenarioParameters(fuel_price_change=change))

    def build_warehouse_outage_scenario(
        self, warehouse_id: str, name: str = "warehouse_outage"
    ) -> Dict:
        return {
            "name": name,
            "type": "outage",
            "affected_warehouse": warehouse_id,
            "description": f"Warehouse {warehouse_id} is offline",
        }

    def build_competitor_scenario(
        self, price_change: float, name: str = "competitor_change"
    ) -> "SimulationConfig":
        return self._apply_params(name, ScenarioParameters())

    def _apply_params(
        self, name: str, params: ScenarioParameters
    ) -> "SimulationConfig":
        new_config = SimulationConfig(
            name=name,
            duration_hours=self.base.duration_hours,
            num_deliveries=int(self.base.num_deliveries * params.demand_multiplier),
            num_drivers=int(self.base.num_drivers * params.driver_availability),
            num_warehouses=self.base.num_warehouses,
            random_seed=self.base.random_seed,
        )

        self.scenarios[name] = params
        return new_config

    def get_scenario(self, name: str) -> Optional[ScenarioParameters]:
        return self.scenarios.get(name)

    def list_scenarios(self) -> Dict:
        return self.scenarios


from src.simulation.framework import SimulationConfig
