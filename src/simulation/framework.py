from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np
import random


@dataclass
class SimulationConfig:
    name: str
    duration_hours: int
    num_deliveries: int
    num_drivers: int
    num_warehouses: int

    weather_enabled: bool = True
    traffic_enabled: bool = True
    demand_variation: float = 1.0

    random_seed: int = 42


class SimulationFramework:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.state: Optional[Dict] = None
        self.history: List[Dict] = []

    def initialize(self):
        random.seed(self.config.random_seed)
        np.random.seed(self.config.random_seed)

        self.state = {
            "deliveries": self._generate_deliveries(),
            "drivers": self._generate_drivers(),
            "warehouses": self._generate_warehouses(),
            "weather": self._generate_weather(),
            "traffic": self._generate_traffic(),
            "time": 0,
            "market_share": 0.5,
            "drivers_available": self.config.num_drivers,
        }

        return self.state

    def _generate_deliveries(self) -> List[Dict]:
        return [
            {
                "id": f"DEL{i:04d}",
                "origin": f"WH{random.randint(1, min(3, self.config.num_warehouses + 1))}",
                "destination": f"LOC{random.randint(1, 50)}",
                "distance_km": np.random.uniform(10, 100),
                "weight_kg": np.random.uniform(1, 50),
                "deadline": random.randint(2, 8),
                "priority": random.choice(["high", "medium", "low"]),
                "status": "pending",
                "estimated_time": 60,
            }
            for i in range(self.config.num_deliveries)
        ]

    def _generate_drivers(self) -> List[Dict]:
        return [
            {
                "id": f"DRV{i:03d}",
                "performance": np.random.uniform(0.6, 1.0),
                "available": True,
                "current_delivery": None,
            }
            for i in range(self.config.num_drivers)
        ]

    def _generate_warehouses(self) -> List[Dict]:
        return [
            {"id": f"WH{i}", "capacity": 100, "current_load": 0, "status": "online"}
            for i in range(1, self.config.num_warehouses + 1)
        ]

    def _generate_weather(self) -> Dict:
        return {
            "condition": "clear",
            "severity": 1,
            "precipitation": 0,
            "visibility": 10,
        }

    def _generate_traffic(self) -> Dict:
        return {"index": 5, "congestion_level": "medium"}

    def step(self, actions: List[Dict] = None):
        self.state["time"] += 1

        self._update_environment()
        self._process_deliveries()

        self.history.append(self._capture_state())

        return self.state

    def _update_environment(self):
        pass

    def _process_deliveries(self):
        pass

    def _capture_state(self) -> Dict:
        return {
            "time": self.state["time"],
            "active_deliveries": len(
                [d for d in self.state["deliveries"] if d.get("status") == "active"]
            ),
            "completed": len(
                [d for d in self.state["deliveries"] if d.get("status") == "completed"]
            ),
            "pending": len(
                [d for d in self.state["deliveries"] if d.get("status") == "pending"]
            ),
        }

    def run_simulation(self):
        self.initialize()

        for hour in range(self.config.duration_hours):
            self.step()

        return self._calculate_metrics()

    def _calculate_metrics(self) -> Dict:
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
            "pending": total - completed - delayed,
            "on_time_rate": completed / total if total > 0 else 0,
            "duration_hours": self.config.duration_hours,
        }


if __name__ == "__main__":
    config = SimulationConfig(
        name="test",
        duration_hours=24,
        num_deliveries=100,
        num_drivers=20,
        num_warehouses=3,
    )
    sim = SimulationFramework(config)
    print("Simulation framework ready")
