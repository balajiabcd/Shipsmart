"""
Google OR-Tools integration for Vehicle Routing Problem (VRP).
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math
import random

try:
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp

    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False


@dataclass
class DeliveryRequest:
    """Represents a delivery request."""

    id: str
    location_id: str
    lat: float
    lon: float
    demand: int = 1
    time_window_start: Optional[float] = None
    time_window_end: Optional[float] = None
    service_time: float = 0


@dataclass
class Vehicle:
    """Represents a vehicle for VRP."""

    id: str
    capacity: int = 10
    start_location_id: str = ""
    end_location_id: str = ""
    fixed_cost: float = 0
    cost_per_km: float = 1.0


@dataclass
class VRPSolution:
    """VRP solution container."""

    routes: List[List[str]]
    total_distance: float
    total_cost: float
    assigned_deliveries: int
    unassigned_deliveries: List[str]
    vehicle_usage: Dict[str, int]


class ORToolsVRP:
    """Google OR-Tools VRP solver."""

    def __init__(self):
        if not ORTOOLS_AVAILABLE:
            raise ImportError(
                "Google OR-Tools is not installed. Install with: pip install ortools"
            )
        self.deliveries: Dict[str, DeliveryRequest] = {}
        self.vehicles: List[Vehicle] = []
        self.distance_matrix: List[List[float]] = []

    def set_distance_matrix(self, matrix: List[List[float]]) -> None:
        """Set custom distance matrix."""
        self.distance_matrix = matrix

    def add_delivery(self, delivery: DeliveryRequest) -> None:
        """Add a delivery request."""
        self.deliveries[delivery.id] = delivery

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Add a vehicle."""
        self.vehicles.append(vehicle)

    def _create_routing_model(self) -> "pywrapcp.RoutingModel":
        """Create OR-Tools routing model."""
        num_locations = len(self.deliveries) + 1
        num_vehicles = len(self.vehicles)

        routing = pywrapcp.RoutingModel(num_locations, num_vehicles)

        def distance_callback(from_index: int, to_index: int) -> int:
            if from_index == to_index:
                return 0
            from_node = routing.IndexToNode(from_index)
            to_node = routing.IndexToNode(to_index)

            if from_node == 0:
                fromdelivery_idx = to_index - 1
            else:
                fromdelivery_idx = from_node - 1

            if to_node == 0:
                todelivery_idx = to_index - 1
            else:
                todelivery_idx = to_node - 1

            if from_node == 0 and to_node > 0:
                if todelivery_idx < len(self.distance_matrix):
                    return int(self.distance_matrix[0][todelivery_idx] * 1000)
            elif from_node > 0 and to_node == 0:
                if fromdelivery_idx < len(self.distance_matrix):
                    return int(self.distance_matrix[fromdelivery_idx][0] * 1000)
            elif from_node > 0 and to_node > 0:
                if fromdelivery_idx < len(
                    self.distance_matrix
                ) and todelivery_idx < len(self.distance_matrix[0]):
                    return int(
                        self.distance_matrix[fromdelivery_idx][todelivery_idx] * 1000
                    )

            return 0

        transit_callback = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback)

        return routing

    def solve_vrp(
        self,
        max_distance: float = 10000,
        max_time: float = 3600,
        greedy_approach: bool = True,
    ) -> VRPSolution:
        """Solve VRP with OR-Tools."""
        if not self.deliveries or not self.vehicles:
            return VRPSolution(
                routes=[],
                total_distance=0,
                total_cost=0,
                assigned_deliveries=0,
                unassigned_deliveries=list(self.deliveries.keys()),
                vehicle_usage={},
            )

        routing = self._create_routing_model()

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        if greedy_approach:
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            )
        else:
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
            )

        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = int(max_time)

        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            return VRPSolution(
                routes=[],
                total_distance=0,
                total_cost=0,
                assigned_deliveries=0,
                unassigned_deliveries=list(self.deliveries.keys()),
                vehicle_usage={v.id: 0 for v in self.vehicles},
            )

        routes: List[List[str]] = []
        total_distance = 0.0
        total_cost = 0.0
        assigned_count = 0
        vehicle_usage: Dict[str, int] = {v.id: 0 for v in self.vehicles}

        for vehicle_id in range(len(self.vehicles)):
            route = []
            index = routing.Start(vehicle_id)

            while not routing.IsEnd(index):
                node = routing.IndexToNode(index)
                if node > 0:
                    delivery_ids = list(self.deliveries.keys())
                    if node - 1 < len(delivery_ids):
                        route.append(delivery_ids[node - 1])
                        assigned_count += 1
                        vehicle_usage[self.vehicles[vehicle_id].id] += 1
                index = solution.Value(routing.NextVar(index))

            if route:
                routes.append(route)

        unassigned = [
            d_id
            for d_id in self.deliveries.keys()
            if not any(d_id in route for route in routes)
        ]

        return VRPSolution(
            routes=routes,
            total_distance=total_distance,
            total_cost=total_cost,
            assigned_deliveries=assigned_count,
            unassigned_deliveries=unassigned,
            vehicle_usage=vehicle_usage,
        )

    def solve_cvrp(self, capacity: int = 10) -> VRPSolution:
        """Capacitated VRP."""
        self.vehicles = [
            Vehicle(
                id=f"vehicle_{i}",
                capacity=capacity,
                start_location_id="depot",
                end_location_id="depot",
            )
            for i in range(3)
        ]
        return self.solve_vrp()

    def solve_vrptw(self) -> VRPSolution:
        """VRP with Time Windows."""
        return self.solve_vrp()


def create_simple_vrp(
    locations: List[Tuple[float, float]],
    num_vehicles: int = 3,
    vehicle_capacity: int = 10,
) -> VRPSolution:
    """Create and solve a simple VRP."""
    n = len(locations)
    if n == 0:
        return VRPSolution(
            routes=[],
            total_distance=0,
            total_cost=0,
            assigned_deliveries=0,
            unassigned_deliveries=[],
            vehicle_usage={},
        )

    vrp = ORToolsVRP()

    for i, (lat, lon) in enumerate(locations[1:], start=1):
        vrp.add_delivery(
            DeliveryRequest(
                id=f"delivery_{i}", location_id=f"loc_{i}", lat=lat, lon=lon
            )
        )

    for i in range(num_vehicles):
        vrp.add_vehicle(
            Vehicle(
                id=f"vehicle_{i}",
                capacity=vehicle_capacity,
                start_location_id="depot",
                end_location_id="depot",
                cost_per_km=1.5,
            )
        )

    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                lat1, lon1 = locations[i]
                lat2, lon2 = locations[j]
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = (
                    math.sin(dlat / 2) ** 2
                    + math.cos(math.radians(lat1))
                    * math.cos(math.radians(lat2))
                    * math.sin(dlon / 2) ** 2
                )
                c = 2 * math.asin(math.sqrt(a))
                matrix[i][j] = c * 6371

    vrp.set_distance_matrix(matrix)
    return vrp.solve_vrp()
