# Milestone #254: Test Route Optimization

**Your Role:** AI/LLM Engineer

Validate routing suggestions:

```python
# tests/test_route_optimization.py

import pytest
import numpy as np
from src.routing.graph import Graph, Node, Edge
from src.routing.dijkstra import Dijkstra
from src.routing.tsp import TSPSolver

@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_node(Node("A", 0, 0, "warehouse"))
    g.add_node(Node("B", 1, 1, "customer"))
    g.add_node(Node("C", 2, 2, "customer"))
    g.add_node(Node("D", 3, 3, "customer"))
    
    g.add_edge(Edge("A", "B", 10, 15))
    g.add_edge(Edge("B", "C", 10, 15))
    g.add_edge(Edge("C", "D", 10, 15))
    g.add_edge(Edge("A", "C", 25, 30))
    g.add_edge(Edge("B", "D", 25, 30))
    
    return g

def test_dijkstra_shortest_path(sample_graph):
    dijkstra = Dijkstra(sample_graph)
    path, distance = dijkstra.find_shortest_path("A", "D")
    
    assert path == ["A", "B", "C", "D"]
    assert distance == 30

def test_tsp_solution():
    distance_matrix = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    
    solver = TSPSolver(distance_matrix)
    route, distance = solver.solve_nearest_neighbor(0)
    
    assert route[0] == 0
    assert len(route) == 5  # Includes return to start
    assert distance < float('inf')

def test_graph_creation():
    g = Graph()
    g.add_node(Node("W1", 40.7128, -74.0060, "warehouse"))
    assert "W1" in g.nodes
```

Run: `pytest tests/test_route_optimization.py -v`

Commit.