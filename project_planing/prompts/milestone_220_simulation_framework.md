# Milestone #220: Design Simulation Framework

**Your Role:** AI/LLM Engineer

Define simulation parameters:

```python
# src/simulation/framework.py

from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np

@dataclass
class SimulationConfig:
    name: str
    duration_hours: int
    num_deliveries: int
    num_drivers: int
    num_warehouses: int
    
    weather_enabled: bool = True
    traffic_enabled: bool = True
    demand_variation: float = 1.0  # Multiplier
    
    random_seed: int = 42

class SimulationFramework:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.state = None
        self.history = []
    
    def initialize(self):
        np.random.seed(self.config.random_seed)
        
        self.state = {
            "deliveries": self._generate_deliveries(),
            "drivers": self._generate_drivers(),
            "warehouses": self._generate_warehouses(),
            "weather": self._generate_weather(),
            "traffic": self._generate_traffic(),
            "time": 0
        }
        
        return self.state
    
    def _generate_deliveries(self) -> List[Dict]:
        return [
            {
                "id": f"DEL{i:04d}",
                "origin": f"WH{random.randint(1, 3)}",
                "destination": f"LOC{random.randint(1, 50)}",
                "distance_km": np.random.uniform(10, 100),
                "weight_kg": np.random.uniform(1, 50),
                "deadline": np.random.randint(2, 8)
            }
            for i in range(self.config.num_deliveries)
        ]
    
    def _generate_drivers(self) -> List[Dict]:
        return [
            {
                "id": f"DRV{i:03d}",
                "performance": np.random.uniform(0.6, 1.0),
                "available": True,
                "current_delivery": None
            }
            for i in range(self.config.num_drivers)
        ]
    
    def _generate_warehouses(self) -> List[Dict]:
        return [
            {"id": f"WH{i}", "capacity": 100, "current_load": 0}
            for i in range(1, self.config.num_warehouses + 1)
        ]
    
    def _generate_weather(self) -> Dict:
        return {"condition": "clear", "severity": 1, "precipitation": 0}
    
    def _generate_traffic(self) -> Dict:
        return {"index": 5, "congestion_level": "medium"}
    
    def step(self, actions: List[Dict] = None):
        """Advance simulation by one hour"""
        self.state["time"] += 1
        
        # Update weather and traffic
        self._update_environment()
        
        # Process deliveries
        self._process_deliveries()
        
        # Record history
        self.history.append(self._capture_state())
        
        return self.state
    
    def _update_environment(self):
        pass  # Override in subclasses
    
    def _process_deliveries(self):
        pass  # Override in subclasses
    
    def _capture_state(self) -> Dict:
        return {
            "time": self.state["time"],
            "active_deliveries": len([d for d in self.state["deliveries"] if d.get("status") == "active"]),
            "completed": len([d for d in self.state["deliveries"] if d.get("status") == "completed"])
        }
```

Commit.