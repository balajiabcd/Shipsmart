"""
Graph data structure for route optimization.
Defines nodes, edges, and graph operations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import math


class TransportMode(Enum):
    ROAD = "road"
    HIGHWAY = "highway"
    RAIL = "rail"
    WATERWAY = "waterway"


@dataclass
class Node:
    """Represents a location node in the graph."""

    id: str
    lat: float
    lon: float
    name: str = ""
    node_type: str = "location"
    metadata: Dict = field(default_factory=dict)

    def distance_to(self, other: "Node") -> float:
        """Calculate haversine distance to another node in km."""
        return haversine_distance(self.lat, self.lon, other.lat, other.lon)


@dataclass
class Edge:
    """Represents a connection between two nodes."""

    source: str
    target: str
    weight: float
    transport_mode: TransportMode = TransportMode.ROAD
    distance_km: float = 0.0
    travel_time_minutes: float = 0.0
    cost: float = 0.0
    road_type: str = "local"
    is_toll_road: bool = False
    toll_cost: float = 0.0
    traffic_factor: float = 1.0
    weather_factor: float = 1.0
    metadata: Dict = field(default_factory=dict)

    @property
    def effective_weight(self) -> float:
        """Calculate effective weight considering conditions."""
        return self.weight * self.traffic_factor * self.weather_factor


class Graph:
    """Directed weighted graph for route optimization."""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}
        self.adjacency: Dict[str, Dict[str, Edge]] = {}

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = []
            self.adjacency[node.id] = {}

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        if edge.source not in self.edges:
            self.edges[edge.source] = []
            self.adjacency[edge.source] = {}

        self.edges[edge.source].append(edge)
        self.adjacency[edge.source][edge.target] = edge

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str) -> List[Node]:
        """Get all neighboring nodes."""
        if node_id not in self.adjacency:
            return []
        neighbor_ids = self.adjacency[node_id].keys()
        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]

    def get_edge(self, source: str, target: str) -> Optional[Edge]:
        """Get edge between two nodes."""
        return self.adjacency.get(source, {}).get(target)

    def has_path(self, source: str, target: str) -> bool:
        """Check if path exists between two nodes."""
        if source == target:
            return True
        if source not in self.adjacency:
            return False
        if target in self.adjacency[source]:
            return True
        visited = set()
        queue = [source]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            if current not in self.adjacency:
                continue
            for neighbor in self.adjacency[current]:
                if neighbor == target:
                    return True
                if neighbor not in visited:
                    queue.append(neighbor)
        return False

    def get_all_nodes(self) -> List[str]:
        """Get all node IDs."""
        return list(self.nodes.keys())

    def node_count(self) -> int:
        """Get number of nodes."""
        return len(self.nodes)

    def edge_count(self) -> int:
        """Get number of edges."""
        return sum(len(edges) for edges in self.edges.values())

    def remove_node(self, node_id: str) -> None:
        """Remove a node and its edges."""
        if node_id in self.nodes:
            del self.nodes[node_id]
        if node_id in self.edges:
            del self.edges[node_id]
        if node_id in self.adjacency:
            del self.adjacency[node_id]
        for source in self.edges:
            self.edges[source] = [e for e in self.edges[source] if e.target != node_id]
            if node_id in self.adjacency[source]:
                del self.adjacency[source][node_id]

    def remove_edge(self, source: str, target: str) -> None:
        """Remove an edge between two nodes."""
        if source in self.edges:
            self.edges[source] = [e for e in self.edges[source] if e.target != target]
        if source in self.adjacency and target in self.adjacency[source]:
            del self.adjacency[source][target]

    def clear(self) -> None:
        """Clear all nodes and edges."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency.clear()


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_travel_time(distance_km: float, avg_speed_kmh: float = 60.0) -> float:
    """Calculate travel time in minutes given distance and average speed."""
    if avg_speed_kmh <= 0:
        return 0
    return (distance_km / avg_speed_kmh) * 60


def estimate_fuel_cost(
    distance_km: float, fuel_efficiency: float = 8.0, fuel_price: float = 1.6
) -> float:
    """Estimate fuel cost in EUR."""
    return (distance_km / 100) * fuel_efficiency * fuel_price
