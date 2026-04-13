# Milestone #253: Create /optimize_route Endpoint

**Your Role:** AI/LLM Engineer

Expose route optimization service:

```python
# api/endpoints/routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/optimize", tags=["Route Optimization"])

class DeliveryRequest(BaseModel):
    id: str
    location_id: str
    weight: float = 1.0
    priority: int = 1

class RouteOptimizationRequest(BaseModel):
    deliveries: List[DeliveryRequest]
    num_vehicles: int = 5
    vehicle_capacity: float = 100.0
    algorithm: str = "or-tools"  # or-tools, dijkstra, tsp

@router.post("/route")
async def optimize_route(request: RouteOptimizationRequest):
    try:
        from src.routing.or_tools import ORToolsVRP
        from src.routing.graph import Graph
        
        graph = Graph()
        graph.load_from_csv('data/nodes.csv', 'data/edges.csv')
        
        if request.algorithm == "or-tools":
            vrp = ORToolsVRP(num_vehicles=request.num_vehicles)
            
            delivery_dicts = [d.dict() for d in request.deliveries]
            result = vrp.solve(delivery_dicts, request.num_vehicles)
            
        elif request.algorithm == "tsp":
            from src.routing.tsp import TSPSolver
            import numpy as np
            matrix = np.random.rand(len(request.deliveries), len(request.deliveries))
            solver = TSPSolver(matrix)
            route, distance = solver.solve_nearest_neighbor()
            result = {"routes": [{"route": route, "distance": distance}]}
        
        else:
            raise ValueError(f"Unknown algorithm: {request.algorithm}")
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/algorithms")
async def list_algorithms():
    return {
        "algorithms": [
            {"name": "or-tools", "description": "Google OR-Tools VRP"},
            {"name": "dijkstra", "description": "Dijkstra shortest path"},
            {"name": "tsp", "description": "Traveling Salesman Problem"},
            {"name": "astar", "description": "A* pathfinding"}
        ]
    }
```

Add to `api/main.py`. Commit.