"""
Multi-route optimization for multiple deliveries.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math

from .graph import Graph, Node, Edge
from .dijkstra import DijkstraRouter
from .a_star import AStarRouter
from .tsp_solver import TSPSolver, TSPSolution


@dataclass
class Delivery:
    """Represents a single delivery."""

    id: str
    location_id: str
    lat: float
    lon: float
    priority: int = 1
    time_window_start: Optional[float] = None
    time_window_end: Optional[float] = None
    estimated_service_time: float = 10


@dataclass
class RoutePlan:
    """A planned route."""

    vehicle_id: str
    deliveries: List[str]
    total_distance: float
    total_time: float
    path: List[str]
    estimated_arrivals: List[float]


@dataclass
class MultiRouteSolution:
    """Solution for multi-route optimization."""

    routes: List[RoutePlan]
    total_distance: float
    total_time: float
    unassigned: List[str]
    utilization: Dict[str, float]


class MultiRouteOptimizer:
    """Optimize routes for multiple vehicles and deliveries."""

    def __init__(self):
        self.graph: Optional[Graph] = None
        self.deliveries: Dict[str, Delivery] = {}
        self.dijkstra = None
        self.a_star = None
        self.tsp_solver = None

    def set_graph(self, graph: Graph) -> None:
        """Set the routing graph."""
        self.graph = graph
        self.dijkstra = DijkstraRouter(graph)
        self.a_star = AStarRouter(graph)
        self.tsp_solver = TSPSolver()
        self.tsp_solver.set_graph(graph)

    def add_delivery(self, delivery: Delivery) -> None:
        """Add a delivery request."""
        self.deliveries[delivery.id] = delivery
        if self.graph and delivery.location_id not in self.graph.nodes:
            self.graph.add_node(
                Node(id=delivery.location_id, lat=delivery.lat, lon=delivery.lon)
            )

    def _calculate_distance_matrix(
        self, locations: List[str]
    ) -> Dict[Tuple[str, str], float]:
        """Calculate distance matrix between all locations."""
        matrix: Dict[Tuple[str, str], float] = {}

        for i, loc_a in enumerate(locations):
            for j, loc_b in enumerate(locations):
                if i == j:
                    matrix[(loc_a, loc_b)] = 0
                else:
                    path = self.dijkstra.find_shortest_path_with_distance(loc_a, loc_b)
                    if path:
                        matrix[(loc_a, loc_b)] = path.total_distance
                    else:
                        node_a = self.graph.get_node(loc_a)
                        node_b = self.graph.get_node(loc_b)
                        if node_a and node_b:
                            matrix[(loc_a, loc_b)] = node_a.distance_to(node_b)
                        else:
                            matrix[(loc_a, loc_b)] = 100

        return matrix

    def optimize_sequential(
        self, depot_id: str, num_vehicles: int = 3
    ) -> MultiRouteSolution:
        """
        Optimize routes sequentially by distance.

        Args:
            depot_id: Depot location ID
            num_vehicles: Number of vehicles

        Returns:
            MultiRouteSolution
        """
        if not self.deliveries:
            return MultiRouteSolution(
                routes=[], total_distance=0, total_time=0, unassigned=[], utilization={}
            )

        delivery_ids = list(self.deliveries.keys())
        locations = [depot_id] + [self.deliveries[d].location_id for d in delivery_ids]
        location_map = {self.deliveries[d].location_id: d for d in delivery_ids}

        if not self.graph:
            return MultiRouteSolution(
                routes=[],
                total_distance=0,
                total_time=0,
                unassigned=delivery_ids,
                utilization={},
            )

        locations_unique = list(set(locations))
        dist_matrix = self._calculate_distance_matrix(locations_unique)

        deliveries_per_vehicle = len(delivery_ids) // num_vehicles + 1
        routes: List[RoutePlan] = []
        total_distance = 0.0
        total_time = 0.0
        assigned = set()

        for v in range(num_vehicles):
            start_idx = v * deliveries_per_vehicle
            end_idx = min(start_idx + deliveries_per_vehicle, len(delivery_ids))

            if start_idx >= len(delivery_ids):
                break

            vehicle_deliveries = delivery_ids[start_idx:end_idx]
            route_locations = [depot_id] + [
                self.deliveries[d].location_id for d in vehicle_deliveries
            ]

            route_path = [depot_id]
            route_distance = 0.0
            route_time = 0.0

            for i in range(len(route_locations) - 1):
                from_loc = route_locations[i]
                to_loc = route_locations[i + 1]

                path = self.dijkstra.find_shortest_path_with_distance(from_loc, to_loc)
                if path and len(path.nodes) > 1:
                    route_path.extend(path.nodes[1:])
                    route_distance += path.total_distance
                    route_time += path.total_time
                else:
                    route_path.append(to_loc)
                    route_distance += dist_matrix.get((from_loc, to_loc), 100)

                assigned.add(vehicle_deliveries[i])

            path_back = self.dijkstra.find_shortest_path_with_distance(
                route_locations[-1], depot_id
            )
            if path_back:
                route_path.extend(path_back.nodes[1:])
                route_distance += path_back.total_distance
                route_time += path_back.total_time

            if vehicle_deliveries:
                routes.append(
                    RoutePlan(
                        vehicle_id=f"vehicle_{v}",
                        deliveries=vehicle_deliveries,
                        total_distance=route_distance,
                        total_time=route_time,
                        path=route_path,
                        estimated_arrivals=[0] * len(vehicle_deliveries),
                    )
                )

            total_distance += route_distance
            total_time += route_time

        unassigned = [d for d in delivery_ids if d not in assigned]

        return MultiRouteSolution(
            routes=routes,
            total_distance=total_distance,
            total_time=total_time,
            unassigned=unassigned,
            utilization={
                v.id: len(v.deliveries) / max(1, deliveries_per_vehicle) for v in routes
            },
        )

    def optimize_balanced(
        self, depot_id: str, num_vehicles: int = 3
    ) -> MultiRouteSolution:
        """
        Optimize routes balancing load across vehicles.

        Args:
            depot_id: Depot location
            num_vehicles: Number of vehicles

        Returns:
            MultiRouteSolution
        """
        solution = self.optimize_sequential(depot_id, num_vehicles)

        if len(solution.routes) <= 1:
            return solution

        max_load = max(len(r.deliveries) for r in solution.routes)
        min_load = min(len(r.deliveries) for r in solution.routes)

        if max_load - min_load <= 1:
            return solution

        all_deliveries = []
        for r in solution.routes:
            all_deliveries.extend(r.deliveries)

        balanced_routes = []
        per_vehicle = len(all_deliveries) // num_vehicles
        remainder = len(all_deliveries) % num_vehicles

        idx = 0
        for v in range(num_vehicles):
            count = per_vehicle + (1 if v < remainder else 0)
            if idx < len(all_deliveries):
                vehicle_deliveries = all_deliveries[idx : idx + count]
                route = (
                    solution.routes[v]
                    if v < len(solution.routes)
                    else RoutePlan(
                        vehicle_id=f"vehicle_{v}",
                        deliveries=[],
                        total_distance=0,
                        total_time=0,
                        path=[depot_id],
                        estimated_arrivals=[],
                    )
                )
                balanced_routes.append(
                    RoutePlan(
                        vehicle_id=route.vehicle_id,
                        deliveries=vehicle_deliveries,
                        total_distance=route.total_distance,
                        total_time=route.total_time,
                        path=route.path,
                        estimated_arrivals=route.estimated_arrivals,
                    )
                )
                idx += count

        return MultiRouteSolution(
            routes=balanced_routes,
            total_distance=solution.total_distance,
            total_time=solution.total_time,
            unassigned=solution.unassigned,
            utilization={
                v.vehicle_id: len(v.deliveries) / max(1, per_vehicle)
                for v in balanced_routes
            },
        )

    def optimize_with_priority(
        self, depot_id: str, num_vehicles: int = 3
    ) -> MultiRouteSolution:
        """
        Optimize routes considering delivery priorities.

        Args:
            depot_id: Depot location
            num_vehicles: Number of vehicles

        Returns:
            MultiRouteSolution
        """
        if not self.deliveries:
            return self.optimize_sequential(depot_id, num_vehicles)

        sorted_deliveries = sorted(
            self.deliveries.items(), key=lambda x: x[1].priority, reverse=True
        )

        temp_optimizer = MultiRouteOptimizer()
        if self.graph:
            temp_optimizer.set_graph(self.graph)

        for d_id, delivery in sorted_deliveries:
            temp_optimizer.add_delivery(delivery)

        return temp_optimizer.optimize_sequential(depot_id, num_vehicles)


def create_route_from_predictions(
    predictions: List[dict], current_lat: float, current_lon: float
) -> MultiRouteSolution:
    """
    Create optimized routes from delay predictions.

    Args:
        predictions: List of prediction dictionaries
        current_lat: Current latitude
        current_lon: Current longitude

    Returns:
        MultiRouteSolution
    """
    optimizer = MultiRouteOptimizer()

    graph = Graph()
    depot_node = Node(
        id="depot", lat=current_lat, lon=current_lon, name="Current Location"
    )
    graph.add_node(depot_node)

    for i, pred in enumerate(predictions):
        delivery = Delivery(
            id=f"delivery_{i}",
            location_id=f"loc_{i}",
            lat=pred.get("lat", 0),
            lon=pred.get("lon", 0),
            priority=pred.get("delay_probability", 0.5),
        )
        optimizer.add_delivery(delivery)

        if delivery.location_id not in graph.nodes:
            graph.add_node(
                Node(id=delivery.location_id, lat=delivery.lat, lon=delivery.lon)
            )

    optimizer.set_graph(graph)

    return optimizer.optimize_balanced(depot_id="depot", num_vehicles=3)
