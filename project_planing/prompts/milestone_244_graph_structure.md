# Milestone #244: Set Up Graph Data Structure

**Your Role:** AI/LLM Engineer

Define nodes and edges:

```python
# src/routing/graph.py

from dataclasses import dataclass
from typing import Dict, List, Tuple
import heapq

@dataclass
class Node:
    id: str
    lat: float
    lon: float
    node_type: str  # warehouse, customer, hub
    metadata: dict = None

@dataclass
class Edge:
    source: str
    destination: str
    distance_km: float
    travel_time_min: float
    traffic_level: str = "medium"

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}
    
    def add_node(self, node: Node):
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = []
    
    def add_edge(self, edge: Edge):
        self.edges[edge.source].append(edge)
    
    def get_neighbors(self, node_id: str) -> List[Edge]:
        return self.edges.get(node_id, [])
    
    def get_edge_weight(self, source: str, dest: str, weight_type: str = "distance") -> float:
        for edge in self.edges.get(source, []):
            if edge.destination == dest:
                if weight_type == "distance":
                    return edge.distance_km
                elif weight_type == "time":
                    return edge.travel_time_min
        return float('inf')
    
    def load_from_csv(self, nodes_path: str, edges_path: str):
        import pandas as pd
        
        nodes_df = pd.read_csv(nodes_path)
        for _, row in nodes_df.iterrows():
            self.add_node(Node(
                id=row['id'],
                lat=row['lat'],
                lon=row['lon'],
                node_type=row['type']
            ))
        
        edges_df = pd.read_csv(edges_path)
        for _, row in edges_df.iterrows():
            self.add_edge(Edge(
                source=row['source'],
                destination=row['destination'],
                distance_km=row['distance_km'],
                travel_time_min=row['travel_time_min']
            ))
```

Commit.