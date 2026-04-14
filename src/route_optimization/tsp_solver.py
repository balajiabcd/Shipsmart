"""
Traveling Salesman Problem (TSP) solver.
"""

from typing import Dict, List, Tuple, Optional
import random
import math
from dataclasses import dataclass

from .graph import Graph
from .dijkstra import Path, DijkstraRouter


@dataclass
class TSPSolution:
    """TSP solution container."""

    route: List[str]
    total_distance: float
    total_time: float
    is_optimal: bool


class TSPSolver:
    """TSP solver with multiple algorithms."""

    def __init__(self):
        self.graph: Optional[Graph] = None
        self.distance_matrix: Dict[Tuple[str, str], float] = {}

    def set_graph(self, graph: Graph) -> None:
        """Set the graph for TSP."""
        self.graph = graph
        self._build_distance_matrix()

    def _build_distance_matrix(self) -> None:
        """Build distance matrix from graph."""
        if not self.graph:
            return

        nodes = self.graph.get_all_nodes()
        for i, node_a in enumerate(nodes):
            for j, node_b in enumerate(nodes):
                if i == j:
                    continue
                edge = self.graph.get_edge(node_a, node_b)
                if edge:
                    self.distance_matrix[(node_a, node_b)] = edge.distance_km
                else:
                    dist = self._estimate_distance(node_a, node_b)
                    self.distance_matrix[(node_a, node_b)] = dist

    def _estimate_distance(self, node_a: str, node_b: str) -> float:
        """Estimate distance using haversine."""
        if not self.graph:
            return 0

        a = self.graph.get_node(node_a)
        b = self.graph.get_node(node_b)
        if not a or not b:
            return 0

        return a.distance_to(b)

    def _get_distance(self, node_a: str, node_b: str) -> float:
        """Get distance between two nodes."""
        key = (node_a, node_b)
        if key in self.distance_matrix:
            return self.distance_matrix[key]
        return self._estimate_distance(node_a, node_b)

    def solve_nearest_neighbor(self, start: str, cities: List[str]) -> TSPSolution:
        """
        Solve TSP using Nearest Neighbor heuristic.

        Args:
            start: Starting city node ID
            cities: List of city node IDs to visit

        Returns:
            TSPSolution
        """
        if start not in cities:
            cities = [start] + cities
        else:
            cities = [start] + [c for c in cities if c != start]

        unvisited = set(cities[1:])
        route = [start]
        total_distance = 0.0
        current = start

        while unvisited:
            nearest = min(unvisited, key=lambda c: self._get_distance(current, c))
            total_distance += self._get_distance(current, nearest)
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        total_distance += self._get_distance(current, start)
        route.append(start)

        return TSPSolution(
            route=route,
            total_distance=total_distance,
            total_time=total_distance / 60 * 60,
            is_optimal=False,
        )

    def solve_greedy(self, start: str, cities: List[str]) -> TSPSolution:
        """
        Solve TSP using Greedy (Nearest Insertion) approach.

        Args:
            start: Starting city
            cities: List of cities to visit

        Returns:
            TSPSolution
        """
        if start not in cities:
            cities = [start] + cities

        route = [start, start]
        total_distance = 0.0
        remaining = set(cities[1:])

        while remaining:
            best_improvement = float("inf")
            best_city = None
            best_pos = None

            for city in remaining:
                for i in range(len(route) - 1):
                    a, b = route[i], route[i + 1]
                    new_dist = self._get_distance(a, city) + self._get_distance(city, b)
                    old_dist = self._get_distance(a, b)
                    improvement = new_dist - old_dist

                    if improvement < best_improvement:
                        best_improvement = improvement
                        best_city = city
                        best_pos = i + 1

            if best_city and best_pos:
                route.insert(best_pos, best_city)
                total_distance += (
                    self._get_distance(route[best_pos - 1], best_city)
                    + self._get_distance(best_city, route[best_pos + 1])
                    - self._get_distance(route[best_pos - 1], route[best_pos + 1])
                )
                remaining.remove(best_city)

        total_distance = sum(
            self._get_distance(route[i], route[i + 1]) for i in range(len(route) - 1)
        )

        return TSPSolution(
            route=route,
            total_distance=total_distance,
            total_time=total_distance / 60,
            is_optimal=False,
        )

    def solve_2opt(
        self, start: str, cities: List[str], max_iterations: int = 1000
    ) -> TSPSolution:
        """
        Solve TSP using 2-opt improvement.

        Args:
            start: Starting city
            cities: List of cities to visit
            max_iterations: Maximum iterations

        Returns:
            TSPSolution
        """
        solution = self.solve_nearest_neighbor(start, cities)
        route = solution.route[:-1]
        improved = True
        iteration = 0

        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            best_i = -1
            best_j = -1
            best_improvement = 0

            for i in range(1, len(route) - 1):
                for j in range(i + 1, len(route)):
                    old_dist = self._get_distance(
                        route[i - 1], route[i]
                    ) + self._get_distance(route[j - 1], route[j])
                    new_dist = self._get_distance(
                        route[i - 1], route[j - 1]
                    ) + self._get_distance(route[i], route[j])

                    improvement = old_dist - new_dist
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_i = i
                        best_j = j

            if best_i > 0 and best_j > 0:
                route[best_i:best_j] = route[best_i:best_j][::-1]
                improved = True

        route.append(start)
        total_distance = sum(
            self._get_distance(route[i], route[i + 1]) for i in range(len(route) - 1)
        )

        return TSPSolution(
            route=route,
            total_distance=total_distance,
            total_time=total_distance / 60,
            is_optimal=False,
        )

    def solve(self, start: str, cities: List[str], method: str = "2opt") -> TSPSolution:
        """
        Solve TSP with specified method.

        Args:
            start: Starting city
            cities: List of cities
            method: Solution method ('nearest', 'greedy', '2opt')

        Returns:
            TSPSolution
        """
        if method == "nearest":
            return self.solve_nearest_neighbor(start, cities)
        elif method == "greedy":
            return self.solve_greedy(start, cities)
        elif method == "2opt":
            return self.solve_2opt(start, cities)
        else:
            return self.solve_nearest_neighbor(start, cities)


def create_tsp_from_coordinates(coordinates: List[Tuple[float, float]]) -> TSPSolution:
    """
    Create and solve TSP from coordinate list.

    Args:
        coordinates: List of (lat, lon) tuples

    Returns:
        TSPSolution
    """
    solver = TSPSolver()

    graph = Graph()
    for i, (lat, lon) in enumerate(coordinates):
        from .graph import Node

        graph.add_node(Node(id=f"city_{i}", lat=lat, lon=lon, name=f"City {i}"))

    solver.set_graph(graph)

    cities = [f"city_{i}" for i in range(len(coordinates))]
    return solver.solve(start=cities[0], cities=cities[1:], method="2opt")
