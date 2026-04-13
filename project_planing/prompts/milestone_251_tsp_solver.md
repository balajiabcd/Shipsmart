# Milestone #251: Implement TSP Solver

**Your Role:** AI/LLM Engineer

Traveling salesman problem:

```python
# src/routing/tsp.py

import itertools
import numpy as np
from typing import List, Tuple

class TSPSolver:
    def __init__(self, distance_matrix: np.ndarray):
        self.distance_matrix = distance_matrix
        self.n = len(distance_matrix)
    
    def solve_exact(self) -> Tuple[List[int], float]:
        best_route = None
        best_distance = float('inf')
        
        for perm in itertools.permutations(range(self.n)):
            distance = self._calculate_route_distance(perm)
            if distance < best_distance:
                best_distance = distance
                best_route = perm
        
        return list(best_route), best_distance
    
    def _calculate_route_distance(self, route: Tuple[int]) -> float:
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i+1]]
        return distance
    
    def solve_nearest_neighbor(self, start: int = 0) -> Tuple[List[int], float]:
        visited = {start}
        route = [start]
        total_distance = 0
        
        current = start
        while len(visited) < self.n:
            nearest = None
            nearest_dist = float('inf')
            
            for j in range(self.n):
                if j not in visited:
                    dist = self.distance_matrix[current][j]
                    if dist < nearest_dist:
                        nearest = j
                        nearest_dist = dist
            
            if nearest is not None:
                route.append(nearest)
                visited.add(nearest)
                total_distance += nearest_dist
                current = nearest
        
        total_distance += self.distance_matrix[current][start]
        route.append(start)
        
        return route, total_distance
    
    def solve_2opt(self, initial_route: List[int] = None) -> Tuple[List[int], float]:
        if initial_route is None:
            route = list(range(self.n))
        else:
            route = initial_route[:-1]  # Remove return to depot
        
        improved = True
        while improved:
            improved = False
            for i in range(len(route) - 1):
                for j in range(i + 2, len(route)):
                    if self._2opt_move_improves(route, i, j):
                        route = self._2opt_move(route, i, j)
                        improved = True
        
        total = self._calculate_route_distance(route) + self.distance_matrix[route[-1]][route[0]]
        return route, total
    
    def _2opt_move_improves(self, route: List[int], i: int, j: int) -> bool:
        before = self.distance_matrix[route[i]][route[i+1]] + self.distance_matrix[route[j-1]][route[j]]
        after = self.distance_matrix[route[i]][route[j-1]] + self.distance_matrix[route[i+1]][route[j]]
        return after < before
    
    def _2opt_move(self, route: List[int], i: int, j: int) -> List[int]:
        new_route = route[:i+1] + route[j-1:i:-1] + route[j:]
        return new_route
```

Commit.