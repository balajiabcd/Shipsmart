"""
Prometheus metrics export for API monitoring.
"""

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/metrics", tags=["monitoring"])

request_count = 0
request_latency_sum = 0.0
endpoint_counts = {}


def record_request(endpoint: str, latency: float):
    """Record a request for metrics."""
    global request_count, request_latency_sum
    request_count += 1
    request_latency_sum += latency

    if endpoint not in endpoint_counts:
        endpoint_counts[endpoint] = 0
    endpoint_counts[endpoint] += 1


@router.get("")
async def get_metrics():
    """Get Prometheus metrics."""
    global request_count, request_latency_sum

    metrics = [
        "# HELP shipsmart_requests_total Total number of API requests",
        "# TYPE shipsmart_requests_total counter",
        f"shipsmart_requests_total {request_count}",
        "",
        "# HELP shipsmart_request_latency_seconds Sum of request latencies",
        "# TYPE shipsmart_request_latency_seconds counter",
        f"shipsmart_request_latency_seconds {request_latency_sum}",
        "",
    ]

    for endpoint, count in endpoint_counts.items():
        safe_name = endpoint.replace("/", "_").strip("_")
        metrics.append(
            f"# HELP shipsmart_endpoint_requests_total Total requests per endpoint"
        )
        metrics.append(f"# TYPE shipsmart_endpoint_requests_total counter")
        metrics.append(
            f'shipsmart_endpoint_requests_total{{endpoint="{endpoint}"}} {count}'
        )

    return PlainTextResponse(content="\n".join(metrics))


@router.get("/summary")
async def get_metrics_summary():
    """Get metrics summary."""
    return {
        "total_requests": request_count,
        "total_latency": request_latency_sum,
        "avg_latency": request_latency_sum / request_count if request_count > 0 else 0,
        "by_endpoint": endpoint_counts,
    }


@router.post("/reset")
async def reset_metrics():
    """Reset metrics."""
    global request_count, request_latency_sum, endpoint_counts
    request_count = 0
    request_latency_sum = 0.0
    endpoint_counts = {}
    return {"status": "metrics reset"}


@router.get("/health")
async def metrics_health():
    """Health check for metrics service."""
    return {
        "status": "healthy",
        "request_count": request_count,
        "timestamp": time.time(),
    }
