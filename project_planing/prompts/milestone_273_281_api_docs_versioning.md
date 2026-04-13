# Milestone #273-281: API Documentation, Versioning, Metrics

```python
# api/main.py - Add docs and versioning

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Shipsmart API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Swagger customisation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(...)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# API Versioning
@app.get("/api/v1/predict/")
async def predict_v1(request: PredictionRequest):
    ...

@app.get("/api/v2/predict/")
async def predict_v2(request: PredictionRequest):
    ...  # Enhanced with more features

# Metrics - Prometheus
from fastapi import Response
import prometheus_client

REQUEST_COUNT = prometheus_client.Counter('requests_total', 'Total requests')
REQUEST_LATENCY = prometheus_client.Histogram('request_latency_seconds', 'Request latency')

@app.get("/metrics")
async def metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )

# Logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error: {exc}")
    return {"detail": "Internal server error"}
```

Commit.