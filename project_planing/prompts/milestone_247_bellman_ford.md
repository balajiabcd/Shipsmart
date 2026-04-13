# Milestone #247: Implement Bellman-Ford

**Your Role:** AI/LLM Engineer

Handle negative weights:

```python
# src/routing/bellman_ford.py

from typing import Dict, List, Tuple

class BellmanFord:
    def __init__(self, graph):
        self.graph = graph
    
    def find_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        distances = {node: float('inf') for node in self.graph.nodes}
        previous = {node: None for node in self.graph.nodes}
        distances[start] = 0
        
        nodes = list(self.graph.nodes)
        edges = []
        for source, edge_list in self.graph.edges.items():
            for edge in edge_list:
                edges.append((source, edge.destination, edge.distance_km))
        
        # Relax edges |V| - 1 times
        for _ in range(len(nodes) - 1):
            for u, v, weight in edges:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
        
        # Check for negative cycles
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                raise ValueError("Negative cycle detected")
        
        path = self._reconstruct_path(previous, start, end)
        return path, distances[end]
    
    def _reconstruct_path(self, previous: Dict, start: str, end: str) -> List[str]:
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        return path if path and path[0] == start else []
```

Commit.