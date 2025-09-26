"""FastAPI application factory with lifespan management.

This module creates and configures the FastAPI application with proper
async context management, middleware, and lifecycle events.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatwait_backend.config import settings
from chatwait_backend.routers import api_router

# Configure logger
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan events.

    Args:
        app: The FastAPI application instance

    Yields:
        None
    """
    # Startup
    logger.info("Starting ChatWait application...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # TODO: Initialize database connections, caches, etc.
    # TODO: Start background tasks
    # TODO: Validate API keys and external service connectivity

    yield

    # Shutdown
    logger.info("Shutting down ChatWait application...")
    # TODO: Close database connections
    # TODO: Stop background tasks
    # TODO: Cleanup resources


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="ChatWait API",
        description="Dual-mode conversational chatbot service",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # TODO: Add trust proxy middleware for proper IP handling when available
    # app.add_middleware(TrustProxyHeadersMiddleware, trusted_hosts=["127.0.0.1", "localhost"])

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    return app


# Create the application instance
app = create_application()


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "service": "chatwait-backend",
        "version": "0.1.0",
        "environment": settings.environment,
    }
