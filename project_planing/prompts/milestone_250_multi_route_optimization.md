# Milestone #250: Create Multi-Route Optimization

**Your Role:** AI/LLM Engineer

Optimize multiple deliveries:

```python
# src/routing/multi_route.py

import numpy as np
from typing import List, Dict

class MultiRouteOptimizer:
    def __init__(self, vrp_solver, graph):
        self.vrp = vrp_solver
        self.graph = graph
    
    def optimize_routes(self, deliveries: List[Dict], num_vehicles: int = 5) -> Dict:
        if not deliveries:
            return {"routes": [], "total_distance": 0}
        
        locations = [d["location_id"] for d in deliveries]
        
        distance_matrix = self._build_distance_matrix(locations)
        
        demands = [d.get("weight", 1) for d in deliveries]
        
        self.vrp.num_vehicles = num_vehicles
        self.vrp.create_model(distance_matrix, demands)
        
        solution = self.vrp.solve()
        
        if solution:
            return self.vrp.format_solution(
                pywrapcp.RoutingIndexManager(len(locations), num_vehicles, 0),
                self.vrp.model, solution
            )
        
        return {"routes": [], "total_distance": float('inf')}
    
    def _build_distance_matrix(self, locations: List[str]) -> np.ndarray:
        n = len(locations)
        matrix = np.zeros((n, n))
        
        from src.routing.dijkstra import Dijkstra
        dijkstra = Dijkstra(self.graph)
        
        for i, loc1 in enumerate(locations):
            for j, loc2 in enumerate(locations):
                if i != j:
                    _, dist = dijkstra.find_shortest_path(loc1, loc2)
                    matrix[i][j] = dist if dist < float('inf') else 1000
        
        return matrix
    
    def assign_vehicles(self, routes: List[Dict], driver_availability: List[str]) -> List[Dict]:
        assigned = []
        
        for i, route in enumerate(routes):
            if i < len(driver_availability):
                route["driver_id"] = driver_availability[i]
                assigned.append(route)
        
        return assigned
```

Commit.