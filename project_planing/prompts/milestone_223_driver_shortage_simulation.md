# Milestone #223: Implement Driver Shortage Simulation

**Your Role:** AI/LLM Engineer

Test driver constraints:

```python
# src/simulation/driver_shortage.py

import numpy as np
from .framework import SimulationFramework

class DriverShortageSimulation(SimulationFramework):
    def __init__(self, config, shortage_percentage: float):
        super().__init__(config)
        self.shortage_percentage = shortage_percentage
    
    def initialize(self):
        super().initialize()
        
        # Reduce available drivers
        available = int(self.config.num_drivers * (1 - self.shortage_percentage))
        for i, driver in enumerate(self.state["drivers"]):
            driver["available"] = i < available
    
    def run_simulation(self):
        self.initialize()
        
        for hour in range(self.config.duration_hours):
            available_drivers = len([d for d in self.state["drivers"] if d["available"]])
            pending = len([d for d in self.state["deliveries"] if d.get("status") == "pending"])
            
            if pending > available_drivers:
                self._handle_driver_shortage(pending - available_drivers)
            
            self.step()
        
        return self._calculate_metrics()
    
    def _handle_driver_shortage(self, deficit: int):
        # Prioritize high-priority deliveries
        pending = [d for d in self.state["deliveries"] if d.get("status") == "pending"]
        pending.sort(key=lambda d: {"high": 0, "medium": 1, "low": 2}[d.get("priority", "medium")])
        
        # Assign best drivers to highest priority
        available_drivers = [d for d in self.state["drivers"] if d["available"]]
        available_drivers.sort(key=lambda d: d["performance"], reverse=True)
        
        for delivery, driver in zip(pending[:len(available_drivers)], available_drivers):
            delivery["status"] = "active"
            delivery["assigned_driver"] = driver["id"]
            driver["available"] = False
    
    def _calculate_metrics(self):
        return {
            "driver_shortage_percentage": self.shortage_percentage * 100,
            "unassigned_deliveries": len([d for d in self.state["deliveries"] if d.get("status") == "pending"])
        }
```

Commit.