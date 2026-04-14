"""
Bellman-Ford algorithm implementation for handling negative weights.
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass

from .graph import Graph, Edge
from .dijkstra import Path


@dataclass
class BellmanFordResult:
    """Result from Bellman-Ford algorithm."""

    distances: Dict[str, float]
    predecessors: Dict[str, Optional[str]]
    has_negative_cycle: bool
    negative_cycle: Optional[List[str]] = None


class BellmanFordRouter:
    """Bellman-Ford algorithm for shortest paths with negative weights."""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.distances: Dict[str, float] = {}
        self.predecessors: Dict[str, Optional[str]] = {}

    def find_shortest_paths(
        self, source: str, weight_func: Callable[[Edge], float] = None
    ) -> BellmanFordResult:
        """
        Find shortest paths from source to all nodes.
        Handles negative edge weights.

        Args:
            source: Source node ID
            weight_func: Custom weight function

        Returns:
            BellmanFordResult with distances and paths
        """
        if weight_func is None:
            weight_func = lambda e: e.effective_weight

        nodes = self.graph.get_all_nodes()

        self.distances = {node: float("inf") for node in nodes}
        self.predecessors = {node: None for node in nodes}

        if source in self.distances:
            self.distances[source] = 0

        for _ in range(len(nodes) - 1):
            updated = False
            for node_id in nodes:
                if self.distances[node_id] == float("inf"):
                    continue
                if node_id not in self.graph.edges:
                    continue
                for edge in self.graph.edges[node_id]:
                    new_dist = self.distances[node_id] + weight_func(edge)
                    if new_dist < self.distances[edge.target]:
                        self.distances[edge.target] = new_dist
                        self.predecessors[edge.target] = node_id
                        updated = True
            if not updated:
                break

        negative_cycle = None
        has_negative_cycle = False
        for node_id in nodes:
            if self.distances[node_id] == float("inf"):
                continue
            if node_id not in self.graph.edges:
                continue
            for edge in self.graph.edges[node_id]:
                if (
                    self.distances[node_id] + weight_func(edge)
                    < self.distances[edge.target]
                ):
                    has_negative_cycle = True
                    negative_cycle = [edge.target, node_id]
                    break
            if has_negative_cycle:
                break

        return BellmanFordResult(
            distances=self.distances.copy(),
            predecessors=self.predecessors.copy(),
            has_negative_cycle=has_negative_cycle,
            negative_cycle=negative_cycle,
        )

    def find_shortest_path(
        self, source: str, target: str, weight_func: Callable[[Edge], float] = None
    ) -> Optional[Path]:
        """Find shortest path from source to target."""
        if weight_func is None:
            weight_func = lambda e: e.effective_weight

        result = self.find_shortest_paths(source, weight_func)

        if result.has_negative_cycle:
            return None

        if target not in result.distances or result.distances[target] == float("inf"):
            return None

        nodes = []
        current = target
        while current is not None:
            nodes.append(current)
            current = result.predecessors[current]
        nodes.reverse()

        edges = []
        total_weight = 0.0
        total_distance = 0.0
        total_time = 0.0

        for i in range(len(nodes) - 1):
            edge = self.graph.get_edge(nodes[i], nodes[i + 1])
            if edge:
                edges.append(edge)
                total_weight += weight_func(edge)
                total_distance += edge.distance_km
                total_time += edge.travel_time_minutes

        return Path(
            nodes=nodes,
            total_weight=total_weight,
            total_distance=total_distance,
            total_time=total_time,
            edges=edges,
        )

    def detect_negative_cycles(self) -> List[List[str]]:
        """Detect all negative weight cycles in the graph."""
        weight_func = lambda e: e.effective_weight
        nodes = self.graph.get_all_nodes()

        distances = {node: 0 for node in nodes}
        predecessors = {node: None for node in nodes}

        for _ in range(len(nodes) - 1):
            for node_id in nodes:
                if node_id not in self.graph.edges:
                    continue
                for edge in self.graph.edges[node_id]:
                    new_dist = distances[node_id] + weight_func(edge)
                    if new_dist < distances[edge.target]:
                        distances[edge.target] = new_dist
                        predecessors[edge.target] = node_id

        negative_cycles = []
        for node_id in nodes:
            if node_id not in self.graph.edges:
                continue
            for edge in self.graph.edges[node_id]:
                if distances[node_id] + weight_func(edge) < distances[edge.target]:
                    cycle = []
                    current = edge.target
                    for _ in range(len(nodes)):
                        current = predecessors[current]
                    if current:
                        cycle.append(current)
                    if cycle and cycle[0] not in cycle[1:]:
                        negative_cycles.append(cycle)

        return negative_cycles
