"""Logging middleware for request/response tracking.

This middleware logs all HTTP requests and responses with structured logging
for monitoring and debugging purposes.
"""

import logging
import time
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware

from chatwait_backend.config import settings

# Configure logger
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or endpoint to call

        Returns:
            The HTTP response
        """
        start_time = time.time()

        # Log request
        request_id = f"{time.time()}-{id(request)}"
        request_body = await self._get_request_body(request)

        log_data = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown"),
        }

        if request_body and settings.log_level == "DEBUG":
            log_data["body"] = request_body

        logger.info("Request started", extra=log_data)

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            error_log_data = log_data.copy()
            error_log_data.update(
                {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "processing_time_ms": int((time.time() - start_time) * 1000),
                }
            )
            logger.error("Request failed", extra=error_log_data)
            raise

        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Log response
        response_log_data = log_data.copy()
        response_log_data.update(
            {
                "status_code": response.status_code,
                "processing_time_ms": processing_time_ms,
            }
        )

        if settings.log_format == "json":
            logger.info("Request completed", extra=response_log_data)
        else:
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"-> {response.status_code} in {processing_time_ms}ms"
            )

        return response

    async def _get_request_body(self, request: Request) -> str:
        """Extract request body for logging.

        Args:
            request: The HTTP request

        Returns:
            Request body as string, or empty string if not available
        """
        try:
            body = await request.body()
            if body:
                return body.decode("utf-8")
        except Exception:
            pass
        return ""

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request.

        Args:
            request: The HTTP request

        Returns:
            Client IP address
        """
        # Check for forwarded IP (behind proxy/load balancer)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Check for real IP
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fall back to client host
        return request.client.host if request.client else "unknown"
