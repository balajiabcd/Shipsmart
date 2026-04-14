"""
Dijkstra algorithm implementation for shortest path finding.
"""

import heapq
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass

from .graph import Graph, Node, Edge


@dataclass
class Path:
    """Represents a path between nodes."""

    nodes: List[str]
    total_weight: float
    total_distance: float
    total_time: float
    edges: List[Edge]

    def to_dict(self) -> dict:
        return {
            "nodes": self.nodes,
            "total_weight": self.total_weight,
            "total_distance": self.total_distance,
            "total_time": self.total_time,
            "edge_count": len(self.edges),
        }


class DijkstraRouter:
    """Dijkstra's algorithm for finding shortest paths."""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.distances: Dict[str, float] = {}
        self.predecessors: Dict[str, Optional[str]] = {}

    def find_shortest_path(
        self, source: str, target: str, weight_func: Callable[[Edge], float] = None
    ) -> Optional[Path]:
        """
        Find shortest path between source and target nodes.

        Args:
            source: Source node ID
            target: Target node ID
            weight_func: Custom weight function (default: edge.effective_weight)

        Returns:
            Path object or None if no path exists
        """
        if weight_func is None:
            weight_func = lambda e: e.effective_weight

        if source not in self.graph.nodes or target not in self.graph.nodes:
            return None

        if source == target:
            node = self.graph.get_node(source)
            edge = Edge(source=source, target=target, weight=0)
            return Path(
                nodes=[source],
                total_weight=0,
                total_distance=0,
                total_time=0,
                edges=[edge],
            )

        self.distances = {source: 0}
        self.predecessors = {source: None}

        pq = [(0, source)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue
            visited.add(current)

            if current == target:
                return self._reconstruct_path(source, target, weight_func)

            if current not in self.graph.adjacency:
                continue

            for neighbor, edge in self.graph.adjacency[current].items():
                if neighbor in visited:
                    continue

                weight = weight_func(edge)
                new_dist = current_dist + weight

                if (
                    neighbor not in self.distances
                    or new_dist < self.distances[neighbor]
                ):
                    self.distances[neighbor] = new_dist
                    self.predecessors[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return None

    def find_shortest_path_with_distance(
        self, source: str, target: str
    ) -> Optional[Path]:
        """Find shortest path by distance."""
        return self.find_shortest_path(
            source, target, weight_func=lambda e: e.distance_km
        )

    def find_shortest_path_with_time(self, source: str, target: str) -> Optional[Path]:
        """Find shortest path by travel time."""
        return self.find_shortest_path(
            source, target, weight_func=lambda e: e.travel_time_minutes
        )

    def find_shortest_path_with_cost(self, source: str, target: str) -> Optional[Path]:
        """Find shortest path by cost."""
        return self.find_shortest_path(
            source, target, weight_func=lambda e: e.cost + e.toll_cost
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
        total_weight = 0
        total_distance = 0
        total_time = 0

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

    def get_all_distances(self, source: str) -> Dict[str, float]:
        """
        Get shortest distances from source to all reachable nodes.
        Uses modified Dijkstra that doesn't stop at target.
        """
        if source not in self.graph.nodes:
            return {}

        self.distances = {source: 0}
        self.predecessors = {source: None}

        pq = [(0, source)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue
            visited.add(current)

            if current not in self.graph.adjacency:
                continue

            for neighbor, edge in self.graph.adjacency[current].items():
                if neighbor in visited:
                    continue

                new_dist = current_dist + edge.effective_weight

                if (
                    neighbor not in self.distances
                    or new_dist < self.distances[neighbor]
                ):
                    self.distances[neighbor] = new_dist
                    self.predecessors[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return self.distances.copy()

    def find_k_shortest_paths(self, source: str, target: str, k: int = 3) -> List[Path]:
        """
        Find k shortest paths using Yen's algorithm.

        Args:
            source: Source node ID
            target: Target node ID
            k: Number of paths to find

        Returns:
            List of up to k Path objects
        """
        if source not in self.graph.nodes or target not in self.graph.nodes:
            return []

        paths = []
        candidates = []

        first_path = self.find_shortest_path(source, target)
        if first_path:
            paths.append(first_path)
        else:
            return []

        for i in range(1, k):
            prev_path = paths[i - 1]

            for j in range(len(prev_path.nodes) - 1):
                spur_node = prev_path.nodes[j]
                root_path = prev_path.nodes[: j + 1]

                removed_edges = set()

                for path in paths:
                    if path.nodes[: j + 1] == root_path:
                        edge = self.graph.get_edge(path.nodes[j], path.nodes[j + 1])
                        if edge:
                            removed_edges.add((path.nodes[j], path.nodes[j + 1]))

                if spur_node in self.graph.nodes:
                    node_id = spur_node
                    if node_id in self.graph.edges:
                        for edge in list(self.graph.edges[node_id]):
                            edge_key = (edge.source, edge.target)
                            if edge_key in removed_edges:
                                self.graph.remove_edge(edge.source, edge.target)

                for node in root_path[:-1]:
                    if node in self.graph.nodes:
                        self.graph.remove_node(node)

                spur_path = self.find_shortest_path(source, spur_node)

                if spur_path:
                    total_weight = spur_path.total_weight

                    if j > 0:
                        root_path_obj = self.find_shortest_path(source, root_path[0])
                        if root_path_obj:
                            total_weight += root_path_obj.total_weight

                    candidate = spur_path
                    if candidate:
                        candidates.append((total_weight, candidate))

                for node in self.graph.get_all_nodes():
                    if node not in [n.id for n in self.graph.nodes.values()]:
                        pass
                    else:
                        break

        candidates.sort(key=lambda x: x[0])
        for _, path in candidates:
            if path not in paths:
                paths.append(path)
                if len(paths) >= k:
                    break

        return paths[:k]
