"""Streaming service for Server-Sent Events (SSE) with reconnection support.

This module provides streaming functionality with token tracking, reconnection
support, and proper SSE formatting for the OpenAI Agents SDK streaming events.
"""

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from chatwait_backend.models.chat_models import (
    StreamEndEvent,
    StreamErrorEvent,
    StreamTokenEvent,
)
from chatwait_backend.services.chat_agent import chat_agent_service

# Configure logger
logger = logging.getLogger(__name__)


class StreamingService:
    """Service for handling SSE streaming with reconnection support."""

    def __init__(self):
        """Initialize streaming service."""
        self.active_connections: dict[str, dict[str, Any]] = {}
        logger.info("StreamingService initialized")

    async def create_stream(
        self, message: str, context_id: str | None = None, last_token_index: int = 0
    ) -> AsyncGenerator[str, None]:
        """Create a streaming response with SSE formatting.

        Args:
            message: User input message
            context_id: Optional conversation context identifier
            last_token_index: Last token index for reconnection

        Yields:
            str: SSE formatted events
        """
        connection_id = f"{context_id or 'default'}-{asyncio.get_event_loop().time()}"
        self.active_connections[connection_id] = {
            "context_id": context_id,
            "last_token_index": last_token_index,
            "created_at": asyncio.get_event_loop().time(),
            "status": "active",
        }

        try:
            logger.info(f"Starting streaming session {connection_id}")

            # Stream tokens from the chat agent
            async for event in chat_agent_service.run_streaming(
                message, context_id, last_token_index
            ):
                if event["type"] == "token":
                    # Format token event as SSE
                    token_event = StreamTokenEvent(
                        token=event["token"],
                        token_index=event["token_index"],
                        context_id=event["context_id"],
                    )
                    yield self._format_sse_event(token_event.model_dump())

                    # Update connection tracking
                    self.active_connections[connection_id]["last_token_index"] = event[
                        "token_index"
                    ]

                elif event["type"] == "end":
                    # Format completion event as SSE
                    end_event = StreamEndEvent(
                        context_id=event["context_id"],
                        final_output=event.get("final_output", ""),
                    )
                    yield self._format_sse_event(end_event.model_dump())

                    # Mark connection as completed
                    self.active_connections[connection_id]["status"] = "completed"
                    logger.info(
                        f"Streaming session {connection_id} completed successfully"
                    )

                elif event["type"] == "error":
                    # Format error event as SSE
                    error_event = StreamErrorEvent(
                        context_id=event.get("context_id"),
                        error_code=event.get("error_code", "UNKNOWN_ERROR"),
                        message=event.get("message", "Unknown error"),
                    )
                    yield self._format_sse_event(error_event.model_dump())

                    # Mark connection as errored
                    self.active_connections[connection_id]["status"] = "error"
                    logger.error(
                        f"Streaming session {connection_id} failed: {event.get('message')}"
                    )

        except Exception as e:
            logger.error(f"Error in streaming service {connection_id}: {e}")

            # Send error event
            error_event = StreamErrorEvent(
                context_id=context_id,
                error_code="STREAMING_SERVICE_ERROR",
                message=str(e),
            )
            yield self._format_sse_event(error_event.model_dump())

            # Mark connection as errored
            self.active_connections[connection_id]["status"] = "error"

        finally:
            # Cleanup connection tracking
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]

    def _format_sse_event(self, data: dict[str, Any]) -> str:
        """Format data as Server-Sent Event.

        Args:
            data: Event data dictionary

        Returns:
            str: SSE formatted event
        """
        # SSE format: "data: <json_data>\n\n"
        json_data = json.dumps(data, ensure_ascii=False)
        return f"data: {json_data}\n\n"

    async def get_connection_status(self, context_id: str) -> dict[str, Any] | None:
        """Get status of streaming connection for reconnection support.

        Args:
            context_id: Conversation context identifier

        Returns:
            Optional[Dict]: Connection status information
        """
        # Find active connection for this context
        for conn_id, conn_data in self.active_connections.items():
            if conn_data["context_id"] == context_id:
                return {
                    "connection_id": conn_id,
                    "context_id": conn_data["context_id"],
                    "last_token_index": conn_data["last_token_index"],
                    "status": conn_data["status"],
                    "created_at": conn_data["created_at"],
                }
        return None

    async def cleanup_abandoned_connections(self, timeout_seconds: int = 300) -> int:
        """Clean up abandoned connections that have timed out.

        Args:
            timeout_seconds: Timeout in seconds (default 5 minutes)

        Returns:
            int: Number of connections cleaned up
        """
        current_time = asyncio.get_event_loop().time()
        cleaned_count = 0

        for conn_id, conn_data in list(self.active_connections.items()):
            if (
                conn_data["status"] == "active"
                and (current_time - conn_data["created_at"]) > timeout_seconds
            ):
                logger.warning(f"Cleaning up abandoned connection {conn_id}")
                del self.active_connections[conn_id]
                cleaned_count += 1

        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} abandoned connections")

        return cleaned_count

    async def health_check(self) -> dict[str, Any]:
        """Check streaming service health.

        Returns:
            Dict: Health status information
        """
        try:
            active_connections = len(self.active_connections)

            return {
                "status": "healthy",
                "active_connections": active_connections,
                "service_available": True,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Streaming service health check failed: {str(e)}",
            }


# Global service instance
streaming_service = StreamingService()
