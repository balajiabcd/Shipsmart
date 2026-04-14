import numpy as np
import random
from .framework import SimulationFramework


class DemandSimulation(SimulationFramework):
    def __init__(self, config, demand_multiplier: float = 1.0):
        super().__init__(config)
        self.demand_multiplier = demand_multiplier

    def _generate_deliveries(self):
        base_count = self.config.num_deliveries
        new_count = int(base_count * self.demand_multiplier)

        deliveries = []
        for i in range(new_count):
            deliveries.append(
                {
                    "id": f"DEL{i:04d}",
                    "origin": f"WH{random.randint(1, self.config.num_warehouses + 1)}",
                    "destination": f"LOC{random.randint(1, 50)}",
                    "distance_km": np.random.uniform(10, 100),
                    "priority": random.choice(
                        ["high", "medium", "low"], p=[0.3, 0.5, 0.2]
                    ),
                    "status": "pending",
                    "estimated_time": 60,
                }
            )

        return deliveries

    def _process_deliveries(self):
        available = len([d for d in self.state["drivers"] if d["available"]])

        pending = [d for d in self.state["deliveries"] if d.get("status") == "pending"]

        if pending and available > 0:
            pending.sort(
                key=lambda d: {"high": 0, "medium": 1, "low": 2}[
                    d.get("priority", "medium")
                ]
            )

            for delivery in pending[:available]:
                delivery["status"] = "active"
                delivery["assigned_driver"] = (
                    f"DRV{random.randint(0, self.config.num_drivers - 1):03d}"
                )

        for delivery in self.state["deliveries"]:
            if delivery.get("status") == "active":
                if random.random() < 0.2:
                    delivery["status"] = "completed"

    def _calculate_metrics(self):
        completed = len(
            [d for d in self.state["deliveries"] if d.get("status") == "completed"]
        )
        delayed = len(
            [d for d in self.state["deliveries"] if d.get("status") == "delayed"]
        )
        total = len(self.state["deliveries"])

        return {
            "total_deliveries": total,
            "completed": completed,
            "delayed": delayed,
            "on_time_rate": completed / total if total > 0 else 0,
            "demand_multiplier": self.demand_multiplier,
        }


class DriverShortageSimulation(SimulationFramework):
    def __init__(self, config, shortage_percentage: float):
        super().__init__(config)
        self.shortage_percentage = shortage_percentage

    def initialize(self):
        super().initialize()

        available = int(self.config.num_drivers * (1 - self.shortage_percentage))
        for i, driver in enumerate(self.state["drivers"]):
            driver["available"] = i < available

        self.state["drivers_available"] = available

    def _process_deliveries(self):
        available_drivers = len([d for d in self.state["drivers"] if d["available"]])
        pending = [d for d in self.state["deliveries"] if d.get("status") == "pending"]

        if pending and available_drivers > 0:
            pending.sort(
                key=lambda d: {"high": 0, "medium": 1, "low": 2}[
                    d.get("priority", "medium")
                ]
            )

            for delivery in pending[:available_drivers]:
                delivery["status"] = "active"
                for driver in self.state["drivers"]:
                    if driver["available"]:
                        delivery["assigned_driver"] = driver["id"]
                        driver["available"] = False
                        break

    def _calculate_metrics(self):
        return {
            "driver_shortage_percentage": self.shortage_percentage * 100,
            "unassigned_deliveries": len(
                [d for d in self.state["deliveries"] if d.get("status") == "pending"]
            ),
            "on_time_rate": len(
                [d for d in self.state["deliveries"] if d.get("status") == "completed"]
            )
            / max(len(self.state["deliveries"]), 1),
        }


class WeatherImpactSimulation(SimulationFramework):
    def __init__(self, config, weather_scenario: str = "clear"):
        super().__init__(config)
        self.weather_scenario = weather_scenario

    def _generate_weather(self):
        scenarios = {
            "clear": {
                "condition": "clear",
                "severity": 1,
                "precipitation": 0,
                "visibility": 10,
            },
            "rain": {
                "condition": "rain",
                "severity": 3,
                "precipitation": 10,
                "visibility": 5,
            },
            "storm": {
                "condition": "storm",
                "severity": 7,
                "precipitation": 50,
                "visibility": 2,
            },
            "snow": {
                "condition": "snow",
                "severity": 5,
                "precipitation": 30,
                "visibility": 3,
            },
            "fog": {
                "condition": "fog",
                "severity": 4,
                "precipitation": 0,
                "visibility": 1,
            },
        }
        return scenarios.get(self.weather_scenario, scenarios["clear"])

    def _update_environment(self):
        weather = self.state["weather"]
        speed_multiplier = max(0.3, 1 - (weather["severity"] / 10))

        for delivery in self.state["deliveries"]:
            if delivery.get("status") == "active":
                original_time = delivery.get("estimated_time", 60)
                delivery["estimated_time"] = original_time / speed_multiplier
                delivery["weather_delay"] = original_time * (1 - speed_multiplier)

    def _calculate_metrics(self):
        weather = self.state["weather"]
        total_delay = sum(
            d.get("weather_delay", 0)
            for d in self.state["deliveries"]
            if d.get("weather_delay", 0) > 0
        )

        return {
            "weather_scenario": self.weather_scenario,
            "weather_severity": weather["severity"],
            "total_delay_minutes": total_delay,
            "affected_deliveries": len(
                [d for d in self.state["deliveries"] if d.get("weather_delay", 0) > 0]
            ),
        }


class FuelPriceSimulation(SimulationFramework):
    def __init__(self, config, price_change_percent: float):
        super().__init__(config)
        self.price_change_percent = price_change_percent
        self.base_fuel_price = 1.50

    def run_simulation(self):
        self.initialize()

        current_fuel_price = self.base_fuel_price * (
            1 + self.price_change_percent / 100
        )

        total_cost = 0
        active_deliveries = [
            d for d in self.state["deliveries"] if d.get("status") == "active"
        ]

        for delivery in active_deliveries:
            distance = delivery.get("distance_km", 50)
            fuel_consumption = distance / 15
            cost = fuel_consumption * current_fuel_price
            total_cost += cost

        return self._calculate_cost_metrics(total_cost, current_fuel_price)

    def _calculate_cost_metrics(self, total_cost: float, fuel_price: float):
        base_cost = (
            total_cost / (1 + self.price_change_percent / 100)
            if self.price_change_percent != 0
            else total_cost
        )

        return {
            "base_fuel_price": self.base_fuel_price,
            "current_fuel_price": fuel_price,
            "price_change_percent": self.price_change_percent,
            "total_fuel_cost": total_cost,
            "cost_increase": total_cost - base_cost if base_cost > 0 else 0,
            "cost_per_delivery": total_cost / max(len(self.state["deliveries"]), 1),
        }


class WarehouseOutageSimulation(SimulationFramework):
    def __init__(self, config, outage_warehouse_id: str):
        super().__init__(config)
        self.outage_warehouse_id = outage_warehouse_id

    def initialize(self):
        super().initialize()

        for wh in self.state["warehouses"]:
            if wh["id"] == self.outage_warehouse_id:
                wh["status"] = "offline"
                wh["offline_at"] = 0

        for delivery in self.state["deliveries"]:
            if delivery.get("origin") == self.outage_warehouse_id:
                delivery["origin"] = self._find_alternative_warehouse()
                delivery["routed"] = True

    def _find_alternative_warehouse(self) -> str:
        available = [
            w["id"] for w in self.state["warehouses"] if w.get("status") != "offline"
        ]
        return available[0] if available else self.state["warehouses"][0]["id"]

    def _calculate_metrics(self):
        rerouted = len([d for d in self.state["deliveries"] if d.get("routed", False)])

        return {
            "outage_warehouse": self.outage_warehouse_id,
            "rerouted_deliveries": rerouted,
            "alternative_warehouses_used": len(
                set(
                    d.get("origin")
                    for d in self.state["deliveries"]
                    if d.get("routed", False)
                )
            ),
        }


class CompetitorSimulation(SimulationFramework):
    def __init__(self, config, competitor_price_change: float = 0):
        super().__init__(config)
        self.competitor_price_change = competitor_price_change

    def run_simulation(self):
        self.initialize()

        if self.competitor_price_change < 0:
            market_share_impact = abs(self.competitor_price_change) * 0.02
            self.state["market_share"] -= market_share_impact
        else:
            market_share_impact = self.competitor_price_change * 0.01
            self.state["market_share"] += market_share_impact

        adjusted_deliveries = int(
            len(self.state["deliveries"]) * (1 + market_share_impact)
        )

        return {
            "competitor_price_change": self.competitor_price_change,
            "market_share_impact": market_share_impact,
            "new_market_share": self.state.get("market_share", 0.5),
            "adjusted_demand": adjusted_deliveries,
        }
