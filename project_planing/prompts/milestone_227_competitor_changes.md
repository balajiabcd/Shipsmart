# Milestone #227: Implement Competitor Changes

**Your Role:** AI/LLM Engineer

Test market dynamics:

```python
# src/simulation/competitor_simulation.py

from .framework import SimulationFramework

class CompetitorSimulation(SimulationFramework):
    def __init__(self, config, competitor_price_change: float = 0):
        super().__init__(config)
        self.competitor_price_change = competitor_price_change
    
    def run_simulation(self):
        self.initialize()
        
        # Simulate market share impact
        if self.competitor_price_change < 0:
            # Competitor lowers prices - lose some customers
            market_share_impact = abs(self.competitor_price_change) * 0.02
            self.state["market_share"] -= market_share_impact
        else:
            # Competitor raises prices - gain customers
            market_share_impact = self.competitor_price_change * 0.01
            self.state["market_share"] += market_share_impact
        
        # Adjust demand based on market share
        adjusted_deliveries = int(len(self.state["deliveries"]) * (1 + market_share_impact))
        
        return {
            "competitor_price_change": self.competitor_price_change,
            "market_share_impact": market_share_impact,
            "new_market_share": self.state.get("market_share", 0.5),
            "adjusted_demand": adjusted_deliveries
        }
```

Commit.