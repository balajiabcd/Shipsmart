# Milestone #226: Implement Warehouse Outage

**Your Role:** AI/LLM Engineer

Test facility failures:

```python
# src/simulation/warehouse_outage.py

from .framework import SimulationFramework

class WarehouseOutageSimulation(SimulationFramework):
    def __init__(self, config, outage_warehouse_id: str):
        super().__init__(config)
        self.outage_warehouse_id = outage_warehouse_id
    
    def initialize(self):
        super().initialize()
        
        # Mark warehouse as offline
        for wh in self.state["warehouses"]:
            if wh["id"] == self.outage_warehouse_id:
                wh["status"] = "offline"
                wh["offline_at"] = 0
        
        # Redirect deliveries from offline warehouse
        for delivery in self.state["deliveries"]:
            if delivery.get("origin") == self.outage_warehouse_id:
                delivery["origin"] = self._find_alternative_warehouse()
                delivery["routed"] = True
    
    def _find_alternative_warehouse(self) -> str:
        available = [w["id"] for w in self.state["warehouses"] if w.get("status") != "offline"]
        return available[0] if available else self.state["warehouses"][0]["id"]
    
    def run_simulation(self):
        self.initialize()
        
        for hour in range(self.config.duration_hours):
            self.step()
        
        return self._calculate_outage_metrics()
    
    def _calculate_outage_metrics(self):
        rerouted = len([d for d in self.state["deliveries"] if d.get("routed", False)])
        
        return {
            "outage_warehouse": self.outage_warehouse_id,
            "rerouted_deliveries": rerouted,
            "alternative_warehouses_used": len(set(
                d.get("origin") for d in self.state["deliveries"] 
                if d.get("routed", False)
            ))
        }
```

Commit.