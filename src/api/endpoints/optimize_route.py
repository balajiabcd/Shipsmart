"""
Route optimization API endpoint.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query
import logging
import math

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from src.route_optimization import (
        Graph,
        Node,
        Edge,
        DijkstraRouter,
        AStarRouter,
        MultiRouteOptimizer,
        TSPSolver,
    )

    ROUTING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Route optimization module not available: {e}")
    ROUTING_AVAILABLE = False
    Graph = None
    Node = None
    Edge = None
    DijkstraRouter = None
    AStarRouter = None
    MultiRouteOptimizer = None
    TSPSolver = None

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/route", tags=["route-optimization"])

_ROUTING_GRAPH = None
_DIJKSTRA_ROUTER = None


class LocationInput(BaseModel):
    id: str
    lat: float
    lon: float
    name: Optional[str] = None


class RouteRequest(BaseModel):
    origin: LocationInput
    destination: LocationInput
    waypoints: Optional[List[LocationInput]] = None
    optimization_type: str = "distance"


class MultiLocationRequest(BaseModel):
    origin: LocationInput
    destinations: List[LocationInput]
    num_vehicles: int = 3
    balance_loads: bool = True


class RouteResponse(BaseModel):
    path: List[str]
    total_distance: float
    total_time: float
    nodes: List[Dict[str, Any]]
    algorithm: str


class MultiRouteResponse(BaseModel):
    routes: List[Dict[str, Any]]
    total_distance: float
    total_time: float
    unassigned: List[str]
    utilization: Dict[str, float]


def _calculate_distance(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(min(1, a)))
    return c * 6371


def _init_routing_graph():
    global _ROUTING_GRAPH, _DIJKSTRA_ROUTER

    if _ROUTING_GRAPH is not None:
        return

    if not ROUTING_AVAILABLE:
        _ROUTING_GRAPH = None
        return

    _ROUTING_GRAPH = Graph()
    locations = {
        "depot": (52.5200, 13.4050),
        "berlin": (52.5200, 13.4050),
        "munich": (48.1351, 11.5820),
        "hamburg": (53.5511, 9.9937),
        "frankfurt": (50.1109, 8.6821),
        "cologne": (50.9375, 6.9603),
    }
    for loc_id, (lat, lon) in locations.items():
        _ROUTING_GRAPH.add_node(
            Node(id=loc_id, lat=lat, lon=lon, name=loc_id.capitalize())
        )

    for id1, (lat1, lon1) in locations.items():
        for id2, (lat2, lon2) in locations.items():
            if id1 != id2:
                dist = _calculate_distance(lat1, lon1, lat2, lon2)
                _ROUTING_GRAPH.add_edge(
                    Edge(
                        source=id1,
                        target=id2,
                        weight=dist,
                        distance_km=dist,
                        travel_time_minutes=(dist / 80) * 60,
                        cost=dist * 0.15,
                    )
                )

    _DIJKSTRA_ROUTER = DijkstraRouter(_ROUTING_GRAPH)


@router.post("/optimize", response_model=RouteResponse)
async def optimize_route(request: RouteRequest):
    """Optimize route between two locations."""
    _init_routing_graph()

    if _ROUTING_GRAPH is None:
        distance = _calculate_distance(
            request.origin.lat,
            request.origin.lon,
            request.destination.lat,
            request.destination.lon,
        )
        return RouteResponse(
            path=[request.origin.id, request.destination.id],
            total_distance=distance,
            total_time=(distance / 80) * 60,
            nodes=[
                {
                    "id": request.origin.id,
                    "lat": request.origin.lat,
                    "lon": request.origin.lon,
                    "name": request.origin.name or request.origin.id,
                },
                {
                    "id": request.destination.id,
                    "lat": request.destination.lat,
                    "lon": request.destination.lon,
                    "name": request.destination.name or request.destination.id,
                },
            ],
            algorithm="haversine",
        )

    for loc in [request.origin, request.destination]:
        if loc.id not in _ROUTING_GRAPH.nodes:
            _ROUTING_GRAPH.add_node(
                Node(id=loc.id, lat=loc.lat, lon=loc.lon, name=loc.name or loc.id)
            )

    path = _DIJKSTRA_ROUTER.find_shortest_path_with_distance(
        request.origin.id, request.destination.id
    )

    if path is None:
        raise HTTPException(status_code=404, detail="No path found")

    nodes_data = []
    for node_id in path.nodes:
        node = _ROUTING_GRAPH.get_node(node_id)
        if node:
            nodes_data.append(
                {"id": node.id, "lat": node.lat, "lon": node.lon, "name": node.name}
            )

    return RouteResponse(
        path=path.nodes,
        total_distance=path.total_distance,
        total_time=path.total_time,
        nodes=nodes_data,
        algorithm="dijkstra",
    )


@router.post("/optimize/multi", response_model=MultiRouteResponse)
async def optimize_multi_route(request: MultiLocationRequest):
    """Optimize routes for multiple deliveries across vehicles."""
    _init_routing_graph()

    total_dist = 0
    routes = []

    for i, dest in enumerate(request.destinations):
        dist = _calculate_distance(
            request.origin.lat, request.origin.lon, dest.lat, dest.lon
        )
        total_dist += dist
        routes.append(
            {
                "vehicle_id": f"v{i % request.num_vehicles}",
                "deliveries": [dest.id],
                "total_distance": dist,
                "total_time": (dist / 80) * 60,
                "path": [request.origin.id, dest.id],
            }
        )

    return MultiRouteResponse(
        routes=routes,
        total_distance=total_dist,
        total_time=(total_dist / 80) * 60,
        unassigned=[],
        utilization={"balanced": request.balance_loads},
    )


@router.get("/health")
async def route_health():
    """Health check for routing service."""
    return {"status": "healthy", "mode": "live" if ROUTING_AVAILABLE else "demo"}
