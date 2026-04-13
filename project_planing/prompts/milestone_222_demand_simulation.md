# Milestone #222: Implement Demand Increase Simulation

**Your Role:** AI/LLM Engineer

Test demand variation:

```python
# src/simulation/demand_simulation.py

import numpy as np
from .framework import SimulationFramework

class DemandSimulation(SimulationFramework):
    def __init__(self, config, demand_multiplier: float):
        super().__init__(config)
        self.demand_multiplier = demand_multiplier
    
    def _generate_deliveries(self):
        base_count = self.config.num_deliveries
        new_count = int(base_count * self.demand_multiplier)
        
        deliveries = []
        for i in range(new_count):
            deliveries.append({
                "id": f"DEL{i:04d}",
                "origin": f"WH{np.random.randint(1, self.config.num_warehouses + 1)}",
                "destination": f"LOC{np.random.randint(1, 50)}",
                "distance_km": np.random.uniform(10, 100),
                "priority": np.random.choice(["high", "medium", "low"], p=[0.3, 0.5, 0.2]),
                "status": "pending"
            })
        
        return deliveries
    
    def run_simulation(self):
        self.initialize()
        
        for hour in range(self.config.duration_hours):
            self.step()
            
            # Check delivery capacity
            active = len([d for d in self.state["deliveries"] if d.get("status") == "active"])
            if active > self.state["drivers_available"] * 3:
                self._trigger_overload_response()
        
        return self._calculate_metrics()
    
    def _trigger_overload_response(self):
        # Reorder by priority
        self.state["deliveries"].sort(key=lambda d: d.get("priority", "low"), reverse=True)
    
    def _calculate_metrics(self):
        completed = len([d for d in self.state["deliveries"] if d.get("status") == "completed"])
        delayed = len([d for d in self.state["deliveries"] if d.get("status") == "delayed"])
        
        return {
            "total_deliveries": len(self.state["deliveries"]),
            "completed": completed,
            "delayed": delayed,
            "on_time_rate": completed / len(self.state["deliveries"]) if self.state["deliveries"] else 0,
            "demand_multiplier": self.demand_multiplier
        }
```

Run:
```python
config = SimulationConfig(name="demand_test", duration_hours=24, num_deliveries=100, num_drivers=20, num_warehouses=3)
sim = DemandSimulation(config, demand_multiplier=2.0)
results = sim.run_simulation()
```

Commit.