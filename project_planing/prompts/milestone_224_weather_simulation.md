# Milestone #224: Implement Weather Impact Simulation

**Your Role:** AI/LLM Engineer

Test weather scenarios:

```python
# src/simulation/weather_impact.py

import numpy as np
from .framework import SimulationFramework

class WeatherImpactSimulation(SimulationFramework):
    def __init__(self, config, weather_scenario: str = "clear"):
        super().__init__(config)
        self.weather_scenario = weather_scenario
    
    def _generate_weather(self):
        scenarios = {
            "clear": {"condition": "clear", "severity": 1, "precipitation": 0, "visibility": 10},
            "rain": {"condition": "rain", "severity": 3, "precipitation": 10, "visibility": 5},
            "storm": {"condition": "storm", "severity": 7, "precipitation": 50, "visibility": 2},
            "snow": {"condition": "snow", "severity": 5, "precipitation": 30, "visibility": 3},
            "fog": {"condition": "fog", "severity": 4, "precipitation": 0, "visibility": 1}
        }
        return scenarios.get(self.weather_scenario, scenarios["clear"])
    
    def _update_environment(self):
        weather = self.state["weather"]
        
        # Adjust driver speed based on weather
        speed_multiplier = max(0.3, 1 - (weather["severity"] / 10))
        
        for delivery in self.state["deliveries"]:
            if delivery.get("status") == "active":
                original_time = delivery.get("estimated_time", 60)
                delivery["estimated_time"] = original_time / speed_multiplier
                delivery["weather_delay"] = original_time * (1 - speed_multiplier)
    
    def run_simulation(self):
        self.initialize()
        
        for hour in range(self.config.duration_hours):
            self.step()
        
        return self._calculate_weather_metrics()
    
    def _calculate_weather_metrics(self):
        weather = self.state["weather"]
        total_delay = sum(
            d.get("weather_delay", 0) 
            for d in self.state["deliveries"] 
            if d.get("status") in ["completed", "delayed"]
        )
        
        return {
            "weather_scenario": self.weather_scenario,
            "weather_severity": weather["severity"],
            "total_delay_minutes": total_delay,
            "affected_deliveries": len([d for d in self.state["deliveries"] if d.get("weather_delay", 0) > 0])
        }
```

Commit.