"""
A* algorithm implementation for heuristic pathfinding.
"""

import heapq
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

from .graph import Graph, Node, Edge
from .dijkstra import Path


@dataclass
class AStarNode:
    """Node for A* priority queue."""

    f_score: float
    g_score: float
    node_id: str

    def __lt__(self, other: "AStarNode") -> bool:
        return self.f_score < other.f_score


class AStarRouter:
    """A* algorithm for optimal pathfinding with heuristics."""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.g_scores: Dict[str, float] = {}
        self.f_scores: Dict[str, float] = {}
        self.predecessors: Dict[str, Optional[str]] = {}

    def heuristic(
        self, node_id: str, target: str, heuristic_type: str = "distance"
    ) -> float:
        """Calculate heuristic estimate to target."""
        if node_id not in self.graph.nodes or target not in self.graph.nodes:
            return float("inf")

        current_node = self.graph.nodes[node_id]
        target_node = self.graph.nodes[target]

        if heuristic_type == "distance":
            return current_node.distance_to(target_node)
        elif heuristic_type == "time":
            return current_node.distance_to(target_node) / 80
        elif heuristic_type == "cost":
            return current_node.distance_to(target_node) * 0.15
        else:
            return current_node.distance_to(target_node)

    def _default_weight(self, edge: Edge) -> float:
        return edge.effective_weight

    def find_shortest_path(
        self,
        source: str,
        target: str,
        weight_func: Callable[[Edge], float] = None,
        heuristic_type: str = "distance",
    ) -> Optional[Path]:
        """Find shortest path using A* algorithm."""
        if weight_func is None:
            weight_func = self._default_weight

        if source not in self.graph.nodes or target not in self.graph.nodes:
            return None

        if source == target:
            return Path(
                nodes=[source], total_weight=0, total_distance=0, total_time=0, edges=[]
            )

        self.g_scores = {source: 0}
        self.f_scores = {source: self.heuristic(source, target, heuristic_type)}
        self.predecessors = {source: None}

        open_set = [AStarNode(self.f_scores[source], 0, source)]
        closed_set: set = set()

        while open_set:
            current = heapq.heappop(open_set)
            current_id = current.node_id

            if current_id in closed_set:
                continue
            closed_set.add(current_id)

            if current_id == target:
                return self._reconstruct_path(source, target, weight_func)

            if current_id not in self.graph.adjacency:
                continue

            for neighbor_id, edge in self.graph.adjacency[current_id].items():
                if neighbor_id in closed_set:
                    continue

                g_score = self.g_scores[current_id] + weight_func(edge)
                h_score = self.heuristic(neighbor_id, target, heuristic_type)
                f_score = g_score + h_score

                if (
                    neighbor_id not in self.g_scores
                    or g_score < self.g_scores[neighbor_id]
                ):
                    self.g_scores[neighbor_id] = g_score
                    self.f_scores[neighbor_id] = f_score
                    self.predecessors[neighbor_id] = current_id
                    heapq.heappush(open_set, AStarNode(f_score, g_score, neighbor_id))

        return None

    def find_shortest_path_by_distance(
        self, source: str, target: str
    ) -> Optional[Path]:
        """Find shortest path by distance using A*."""
        return self.find_shortest_path(
            source,
            target,
            weight_func=lambda e: e.distance_km,
            heuristic_type="distance",
        )

    def find_shortest_path_by_time(self, source: str, target: str) -> Optional[Path]:
        """Find shortest path by time using A*."""
        return self.find_shortest_path(
            source,
            target,
            weight_func=lambda e: e.travel_time_minutes,
            heuristic_type="time",
        )

    def find_shortest_path_with_traffic(
        self, source: str, target: str
    ) -> Optional[Path]:
        """Find shortest path considering traffic conditions."""
        return self.find_shortest_path(
            source, target, weight_func=self._default_weight, heuristic_type="distance"
        )

    def _reconstruct_path(
        self, source: str, target: str, weight_func: Callable[[Edge], float]
    ) -> Path:
        """Reconstruct path from predecessors."""
        nodes = []
        current = target
        while current is not None:
            nodes.append(current)
            current = self.predecessors[current]
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

    def get_path_with_waypoints(
        self,
        source: str,
        target: str,
        waypoints: List[str],
        weight_func: Callable[[Edge], float] = None,
    ) -> Optional[List[Path]]:
        """Find paths through intermediate waypoints."""
        if weight_func is None:
            weight_func = self._default_weight

        all_points = [source] + waypoints + [target]
        paths: List[Path] = []

        for i in range(len(all_points) - 1):
            path = self.find_shortest_path(
                all_points[i], all_points[i + 1], weight_func, heuristic_type="distance"
            )
            if path is None:
                return None
            paths.append(path)

        return paths
