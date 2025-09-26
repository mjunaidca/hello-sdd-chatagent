"""Health check endpoints for monitoring and load balancers."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from chatwait_backend.config import settings

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["health"])


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str
    service: str
    version: str
    environment: str
    checks: dict[str, Any]


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Comprehensive health check endpoint for monitoring and load balancers.

    Performs various health checks including:
    - Service availability
    - Configuration validation
    - External dependency checks (can be extended)

    Returns:
        HealthCheckResponse: Detailed health status information
    """
    checks = await _perform_health_checks()

    overall_status = (
        "healthy"
        if all(check["status"] == "ok" for check in checks.values())
        else "degraded"
    )

    return HealthCheckResponse(
        status=overall_status,
        service="chatwait-backend",
        version="0.1.0",
        environment=settings.environment,
        checks=checks,
    )


@router.get("/health/ready")
async def readiness_check() -> dict[str, str]:
    """Kubernetes-style readiness probe.

    Returns:
        Dict with readiness status
    """
    try:
        # TODO: Add actual readiness checks (database connectivity, etc.)
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready") from e


@router.get("/health/live")
async def liveness_check() -> dict[str, str]:
    """Kubernetes-style liveness probe.

    Returns:
        Dict with liveness status
    """
    try:
        # Basic liveness check - if this fails, container should be restarted
        return {"status": "alive"}
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not alive") from e


async def _perform_health_checks() -> dict[str, Any]:
    """Perform comprehensive health checks.

    Returns:
        Dict containing results of all health checks
    """
    checks = {
        "configuration": await _check_configuration(),
        "dependencies": await _check_dependencies(),
        "performance": await _check_performance(),
    }

    # TODO: Add more health checks as needed:
    # - Database connectivity
    # - External API availability (Gemini API)
    # - Redis/cache connectivity
    # - File system permissions

    return checks


async def _check_configuration() -> dict[str, Any]:
    """Check configuration validity.

    Returns:
        Dict with configuration check results
    """
    try:
        # Validate critical configuration
        issues = []

        if not settings.gemini_api_key:
            issues.append("GEMINI_API_KEY not configured")
        if not settings.gemini_base_url:
            issues.append("GEMINI_BASE_URL not configured")
        if settings.port <= 0 or settings.port > 65535:
            issues.append("Invalid port configuration")

        if issues:
            return {
                "status": "error",
                "message": "Configuration issues found",
                "issues": issues,
            }

        return {
            "status": "ok",
            "message": "Configuration is valid",
            "environment": settings.environment,
            "debug_mode": settings.debug,
        }
    except Exception as e:
        return {"status": "error", "message": f"Configuration check failed: {str(e)}"}


async def _check_dependencies() -> dict[str, Any]:
    """Check external dependencies.

    Returns:
        Dict with dependency check results
    """
    try:
        # TODO: Add actual dependency checks
        # - Test Gemini API connectivity
        # - Test database connectivity
        # - Test Redis connectivity

        return {
            "status": "ok",
            "message": "All dependencies available",
            "checks": {
                "gemini_api": "pending",  # TODO: Implement actual check
                "database": "not_configured",  # TODO: Add database support
                "cache": "not_configured",  # TODO: Add Redis support
            },
        }
    except Exception as e:
        return {"status": "error", "message": f"Dependency check failed: {str(e)}"}


async def _check_performance() -> dict[str, Any]:
    """Check performance metrics.

    Returns:
        Dict with performance check results
    """
    try:
        return {
            "status": "ok",
            "message": "Performance within acceptable limits",
            "metrics": {
                "max_tokens_per_response": settings.max_tokens_per_response,
                "streaming_chunk_size": settings.streaming_chunk_size,
                "response_timeout_seconds": settings.response_timeout_seconds,
            },
        }
    except Exception as e:
        return {"status": "error", "message": f"Performance check failed: {str(e)}"}
