"""
Shipsmart FastAPI Application
Main entry point for the Shipsmart API.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .endpoints import (
    predict,
    recommend,
    explain,
    chat,
    simulate,
    alerts,
    optimize_route,
)
from . import auth, metrics

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan context manager."""
    logger.info("Starting Shipsmart API...")
    yield
    logger.info("Shutting down Shipsmart API...")


app = FastAPI(
    title="Shipsmart API",
    description="AI-Powered Delivery Delay Prediction System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred",
        },
    )


app.include_router(predict.router, prefix="/api/v1")
app.include_router(recommend.router, prefix="/api/v1")
app.include_router(explain.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(simulate.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(optimize_route.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Shipsmart API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/v1/health")
async def api_health():
    """API v1 health check."""
    return {"status": "healthy", "api_version": "v1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
