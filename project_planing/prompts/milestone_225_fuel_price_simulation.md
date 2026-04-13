# Milestone #225: Implement Fuel Price Changes

**Your Role:** AI/LLM Engineer

Test cost variations:

```python
# src/simulation/fuel_price.py

from .framework import SimulationFramework

class FuelPriceSimulation(SimulationFramework):
    def __init__(self, config, price_change_percent: float):
        super().__init__(config)
        self.price_change_percent = price_change_percent
        self.base_fuel_price = 1.50  # per liter
    
    def run_simulation(self):
        self.initialize()
        
        current_fuel_price = self.base_fuel_price * (1 + self.price_change_percent / 100)
        
        total_cost = 0
        for delivery in self.state["deliveries"]:
            if delivery.get("status") == "active":
                distance = delivery.get("distance_km", 50)
                fuel_consumption = distance / 15  # liters per 15km
                cost = fuel_consumption * current_fuel_price
                total_cost += cost
        
        return self._calculate_cost_metrics(total_cost, current_fuel_price)
    
    def _calculate_cost_metrics(self, total_cost: float, fuel_price: float):
        base_cost = total_cost / (1 + self.price_change_percent / 100)
        
        return {
            "base_fuel_price": self.base_fuel_price,
            "current_fuel_price": fuel_price,
            "price_change_percent": self.price_change_percent,
            "total_fuel_cost": total_cost,
            "cost_increase": total_cost - base_cost,
            "cost_per_delivery": total_cost / len(self.state["deliveries"])
        }
```

Commit.