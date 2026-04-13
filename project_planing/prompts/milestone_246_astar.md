# Milestone #246: Implement A* Algorithm

**Your Role:** AI/LLM Engineer

Heuristic pathfinding:

```python
# src/routing/astar.py

import heapq
from typing import Dict, List, Tuple, Callable

class AStar:
    def __init__(self, graph, heuristic: Callable = None):
        self.graph = graph
        self.heuristic = heuristic or self._default_heuristic
    
    def _default_heuristic(self, node: str, goal: str) -> float:
        node_obj = self.graph.nodes.get(node)
        goal_obj = self.graph.nodes.get(goal)
        
        if not node_obj or not goal_obj:
            return 0
        
        import math
        return self._haversine(
            node_obj.lat, node_obj.lon,
            goal_obj.lat, goal_obj.lon
        )
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        import math
        R = 6371  # Earth radius in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.asin(math.sqrt(a))
    
    def find_path(self, start: str, end: str, weight_type: str = "distance") -> Tuple[List[str], float]:
        if start not in self.graph.nodes or end not in self.graph.nodes:
            return [], float('inf')
        
        g_score = {node: float('inf') for node in self.graph.nodes}
        g_score[start] = 0
        
        f_score = {node: float('inf') for node in self.graph.nodes}
        f_score[start] = self.heuristic(start, end)
        
        came_from = {node: None for node in self.graph.nodes}
        
        open_set = [(f_score[start], start)]
        closed_set = set()
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == end:
                path = self._reconstruct_path(came_from, start, end)
                return path, g_score[end]
            
            if current in closed_set:
                continue
            closed_set.add(current)
            
            for edge in self.graph.get_neighbors(current):
                if edge.destination in closed_set:
                    continue
                
                weight = self.graph.get_edge_weight(current, edge.destination, weight_type)
                tentative_g = g_score[current] + weight
                
                if tentative_g < g_score[edge.destination]:
                    came_from[edge.destination] = current
                    g_score[edge.destination] = tentative_g
                    f_score[edge.destination] = tentative_g + self.heuristic(edge.destination, end)
                    heapq.heappush(open_set, (f_score[edge.destination], edge.destination))
        
        return [], float('inf')
    
    def _reconstruct_path(self, came_from: Dict, start: str, end: str) -> List[str]:
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = came_from[current]
        
        path.reverse()
        return path if path and path[0] == start else []
```

Commit.