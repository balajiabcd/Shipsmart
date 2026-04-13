# Milestone #229: Create /simulate API Endpoint

**Your Role:** AI/LLM Engineer

Expose simulation service:

```python
# api/endpoints/simulation.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/simulate", tags=["Simulation"])

class SimulationRequest(BaseModel):
    scenario_type: str  # demand, driver_shortage, weather, fuel, warehouse, competitor
    parameters: dict
    
class ScenarioResult(BaseModel):
    scenario: str
    metrics: dict

@router.post("/")
async def run_simulation(request: SimulationRequest):
    try:
        from src.simulation.framework import SimulationConfig
        from src.simulation import (
            DemandSimulation, DriverShortageSimulation,
            WeatherImpactSimulation, FuelPriceSimulation,
            WarehouseOutageSimulation, CompetitorSimulation
        )
        
        config = SimulationConfig(
            name=request.scenario_type,
            duration_hours=request.parameters.get("duration", 24),
            num_deliveries=request.parameters.get("deliveries", 100),
            num_drivers=request.parameters.get("drivers", 20),
            num_warehouses=3
        )
        
        if request.scenario_type == "demand":
            sim = DemandSimulation(config, request.parameters.get("multiplier", 1.0))
        elif request.scenario_type == "driver_shortage":
            sim = DriverShortageSimulation(config, request.parameters.get("shortage", 0.2))
        elif request.scenario_type == "weather":
            sim = WeatherImpactSimulation(config, request.parameters.get("weather", "rain"))
        elif request.scenario_type == "fuel":
            sim = FuelPriceSimulation(config, request.parameters.get("price_change", 10))
        elif request.scenario_type == "warehouse":
            sim = WarehouseOutageSimulation(config, request.parameters.get("warehouse_id", "WH1"))
        elif request.scenario_type == "competitor":
            sim = CompetitorSimulation(config, request.parameters.get("price_change", 0))
        else:
            raise HTTPException(status_code=400, detail="Unknown scenario type")
        
        results = sim.run_simulation()
        
        return {
            "scenario": request.scenario_type,
            "parameters": request.parameters,
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scenarios")
async def list_scenarios():
    return {
        "scenarios": [
            {"type": "demand", "description": "Test demand variation"},
            {"type": "driver_shortage", "description": "Test driver constraints"},
            {"type": "weather", "description": "Test weather impact"},
            {"type": "fuel", "description": "Test fuel price changes"},
            {"type": "warehouse", "description": "Test warehouse outage"},
            {"type": "competitor", "description": "Test market dynamics"}
        ]
    }
```

Add to `api/main.py`. Commit.