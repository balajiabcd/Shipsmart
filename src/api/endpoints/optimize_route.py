"""
Route optimization API endpoint.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query

from ....route_optimization import (
    Graph,
    Node,
    Edge,
    DijkstraRouter,
    AStarRouter,
    MultiRouteOptimizer,
    MultiRouteSolution,
    TSPSolver,
    TSPSolution,
    create_route_from_predictions,
)


router = APIRouter(prefix="/route", tags=["route-optimization"])

_ROUTING_GRAPH = None
_DIJKSTRA_ROUTER = None
_ASTAR_ROUTER = None
_MULTI_ROUTE_OPTIMIZER = None
_TSP_SOLVER = None


class LocationInput(BaseModel):
    """Input for a location."""

    id: str = Field(..., description="Location ID")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    name: Optional[str] = Field(None, description="Location name")


class RouteRequest(BaseModel):
    """Request for route optimization."""

    origin: LocationInput = Field(..., description="Origin location")
    destination: LocationInput = Field(..., description="Destination location")
    waypoints: Optional[List[LocationInput]] = Field(
        default=None, description="Optional waypoints"
    )
    optimization_type: str = Field(
        default="distance", description="Optimization type: distance, time, cost"
    )


class MultiLocationRequest(BaseModel):
    """Request for multi-route optimization."""

    origin: LocationInput = Field(..., description="Origin/Depot location")
    destinations: List[LocationInput] = Field(..., description="Destination locations")
    num_vehicles: int = Field(default=3, ge=1, le=10)
    balance_loads: bool = Field(default=True)


class TSPRequest(BaseModel):
    """Request for TSP solving."""

    locations: List[LocationInput] = Field(..., description="Locations to visit")
    start_location: Optional[str] = Field(None, description="Starting location ID")
    method: str = Field(default="2opt")


class RouteResponse(BaseModel):
    """Response for route optimization."""

    path: List[str]
    total_distance: float
    total_time: float
    nodes: List[Dict[str, Any]]
    algorithm: str


class MultiRouteResponse(BaseModel):
    """Response for multi-route optimization."""

    routes: List[Dict[str, Any]]
    total_distance: float
    total_time: float
    unassigned: List[str]
    utilization: Dict[str, float]


class TSPResponse(BaseModel):
    """Response for TSP solving."""

    route: List[str]
    total_distance: float
    total_time: float
    method: str


def _init_routing_graph():
    """Initialize routing graph with default German routes."""
    global \
        _ROUTING_GRAPH, \
        _DIJKSTRA_ROUTER, \
        _ASTAR_ROUTER, \
        _MULTI_ROUTE_OPTIMIZER, \
        _TSP_SOLVER

    if _ROUTING_GRAPH is not None:
        return

    _ROUTING_GRAPH = Graph()

    locations = {
        "depot": (52.5200, 13.4050),
        "berlin": (52.5200, 13.4050),
        "munich": (48.1351, 11.5820),
        "hamburg": (53.5511, 9.9937),
        "frankfurt": (50.1109, 8.6821),
        "cologne": (50.9375, 6.9603),
        "stuttgart": (48.7758, 9.1829),
        "dusseldorf": (51.2277, 6.7766),
        "dortmund": (51.5136, 7.4653),
        "essen": (51.4556, 7.0117),
        "leipzig": (51.3397, 12.3731),
        "bremen": (53.0793, 8.8017),
        "dresden": (51.0504, 13.7373),
        "hannover": (52.3759, 9.7320),
        "nuremberg": (49.4521, 11.0767),
    }

    for loc_id, (lat, lon) in locations.items():
        _ROUTING_GRAPH.add_node(
            Node(id=loc_id, lat=lat, lon=lon, name=loc_id.capitalize())
        )

    import math

    for id1, (lat1, lon1) in locations.items():
        for id2, (lat2, lon2) in locations.items():
            if id1 != id2:
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = (
                    math.sin(dlat / 2) ** 2
                    + math.cos(math.radians(lat1))
                    * math.cos(math.radians(lat2))
                    * math.sin(dlon / 2) ** 2
                )
                c = 2 * math.asin(math.sqrt(min(1, a)))
                dist = c * 6371

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
    _ASTAR_ROUTER = AStarRouter(_ROUTING_GRAPH)
    _MULTI_ROUTE_OPTIMIZER = MultiRouteOptimizer()
    _MULTI_ROUTE_OPTIMIZER.set_graph(_ROUTING_GRAPH)
    _TSP_SOLVER = TSPSolver()
    _TSP_SOLVER.set_graph(_ROUTING_GRAPH)


@router.post("/optimize", response_model=RouteResponse)
async def optimize_route(request: RouteRequest):
    """Optimize route between two locations."""
    _init_routing_graph()

    waypoint_ids = []
    if request.waypoints:
        for wp in request.waypoints:
            if wp.id not in _ROUTING_GRAPH.nodes:
                _ROUTING_GRAPH.add_node(
                    Node(id=wp.id, lat=wp.lat, lon=wp.lon, name=wp.name or wp.id)
                )
            waypoint_ids.append(wp.id)

    origin_id = request.origin.id
    dest_id = request.destination.id

    for loc in [request.origin, request.destination]:
        if loc.id not in _ROUTING_GRAPH.nodes:
            _ROUTING_GRAPH.add_node(
                Node(id=loc.id, lat=loc.lat, lon=loc.lon, name=loc.name or loc.id)
            )

    if request.optimization_type == "time":
        path = _DIJKSTRA_ROUTER.find_shortest_path_with_time(origin_id, dest_id)
    elif request.optimization_type == "cost":
        path = _DIJKSTRA_ROUTER.find_shortest_path_with_cost(origin_id, dest_id)
    else:
        path = _DIJKSTRA_ROUTER.find_shortest_path_with_distance(origin_id, dest_id)

    if path is None:
        raise HTTPException(status_code=404, detail="No path found between locations")

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

    depot = request.origin
    if depot.id not in _ROUTING_GRAPH.nodes:
        _ROUTING_GRAPH.add_node(
            Node(id=depot.id, lat=depot.lat, lon=depot.lon, name=depot.name or depot.id)
        )

    from ....route_optimization import Delivery

    for dest in request.destinations:
        if dest.id not in _ROUTING_GRAPH.nodes:
            _ROUTING_GRAPH.add_node(
                Node(id=dest.id, lat=dest.lat, lon=dest.lon, name=dest.name or dest.id)
            )

        _MULTI_ROUTE_OPTIMIZER.add_delivery(
            Delivery(id=dest.id, location_id=dest.id, lat=dest.lat, lon=dest.lon)
        )

    if request.balance_loads:
        solution = _MULTI_ROUTE_OPTIMIZER.optimize_balanced(
            depot.id, request.num_vehicles
        )
    else:
        solution = _MULTI_ROUTE_OPTIMIZER.optimize_sequential(
            depot.id, request.num_vehicles
        )

    routes_data = []
    for route in solution.routes:
        routes_data.append(
            {
                "vehicle_id": route.vehicle_id,
                "deliveries": route.deliveries,
                "total_distance": route.total_distance,
                "total_time": route.total_time,
                "path": route.path,
            }
        )

    return MultiRouteResponse(
        routes=routes_data,
        total_distance=solution.total_distance,
        total_time=solution.total_time,
        unassigned=solution.unassigned,
        utilization=solution.utilization,
    )


@router.post("/tsp", response_model=TSPResponse)
async def solve_tsp(request: TSPRequest):
    """Solve Traveling Salesman Problem."""
    _init_routing_graph()

    for loc in request.locations:
        if loc.id not in _ROUTING_GRAPH.nodes:
            _ROUTING_GRAPH.add_node(
                Node(id=loc.id, lat=loc.lat, lon=loc.lon, name=loc.name or loc.id)
            )

    location_ids = [loc.id for loc in request.locations]
    start = request.start_location or location_ids[0]

    solution = _TSP_SOLVER.solve(
        start,
        location_ids[1:] if start in location_ids else location_ids,
        request.method,
    )

    return TSPResponse(
        route=solution.route,
        total_distance=solution.total_distance,
        total_time=solution.total_time,
        method=request.method,
    )


@router.get("/health")
async def route_health():
    """Health check for routing service."""
    _init_routing_graph()
    return {
        "status": "healthy",
        "nodes": _ROUTING_GRAPH.node_count(),
        "edges": _ROUTING_GRAPH.edge_count(),
    }


@router.post("/from-predictions")
async def optimize_from_predictions(predictions: List[Dict[str, Any]]):
    """Create optimized routes from delay predictions."""
    _init_routing_graph()

    current_lat = predictions[0].get("current_lat", 52.52) if predictions else 52.52
    current_lon = predictions[0].get("current_lon", 13.405) if predictions else 13.405

    solution = create_route_from_predictions(predictions, current_lat, current_lon)

    routes_data = []
    for route in solution.routes:
        routes_data.append(
            {
                "vehicle_id": route.vehicle_id,
                "deliveries": route.deliveries,
                "total_distance": route.total_distance,
                "total_time": route.total_time,
            }
        )

    return {
        "routes": routes_data,
        "total_distance": solution.total_distance,
        "total_time": solution.total_time,
        "unassigned": solution.unassigned,
    }
