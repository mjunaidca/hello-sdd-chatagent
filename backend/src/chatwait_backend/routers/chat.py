"""Chat endpoints for wait and streaming modes.

This module implements the /chat/wait and /chat/streaming endpoints
using the OpenAI Agents SDK and custom streaming service.
"""

import json
import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from chatwait_backend.models.chat_models import (
    ChatWaitRequest,
    ChatWaitResponse,
)
from chatwait_backend.services.chat_agent import chat_agent_service
from chatwait_backend.services.streaming_service import streaming_service

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


@router.post("/wait", response_model=ChatWaitResponse)
async def chat_wait(request: ChatWaitRequest) -> dict[str, Any]:
    """Synchronous chat endpoint - returns complete response after generation.

    Args:
        request: ChatWaitRequest with user message and optional context

    Returns:
        ChatWaitResponse: Complete response with metadata
    """
    try:
        start_time = time.time()

        logger.info(
            f"Processing chat wait request: message_length={len(request.message)}"
        )

        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "EMPTY_MESSAGE",
                    "message": "Message cannot be empty. Please provide a valid message.",
                },
            )

        # Run agent synchronously
        result = await chat_agent_service.run_sync(
            message=request.message.strip(), context_id=request.context_id
        )

        processing_time_ms = (time.time() - start_time) * 1000

        logger.info(
            f"Chat wait completed in {processing_time_ms:.2f}ms, "
            f"tokens: {result['token_count']}"
        )

        return ChatWaitResponse(
            message=result["message"],
            context_id=result["context_id"],
            token_count=result["token_count"],
            processing_time_ms=processing_time_ms,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat wait endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "CHAT_WAIT_ERROR",
                "message": "An error occurred while processing your request.",
            },
        ) from e


@router.get("/streaming")
async def chat_streaming(
    message: str,
    context_id: str | None = None,
    last_token_index: int = 0,
):
    """Streaming chat endpoint - returns Server-Sent Events with incremental tokens.

    Args:
        message: User message (required)
        context_id: Optional conversation context identifier
        last_token_index: Last token index for reconnection (default: 0)

    Returns:
        StreamingResponse: SSE stream with incremental tokens
    """
    try:
        logger.info(
            f"Starting streaming chat: message_length={len(message)}, "
            f"context_id={context_id}, last_token_index={last_token_index}"
        )

        # Validate input
        if not message or not message.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "EMPTY_MESSAGE",
                    "message": "Message cannot be empty. Please provide a valid message.",
                },
            )

        # Create streaming response
        async def generate_stream():
            async for event_data in streaming_service.create_stream(
                message=message.strip(),
                context_id=context_id,
                last_token_index=last_token_index,
            ):
                yield event_data

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat streaming endpoint: {e}")
        # Return error as SSE event
        error_data = {
            "type": "error",
            "context_id": context_id,
            "error_code": "CHAT_STREAMING_ERROR",
            "message": "An error occurred while streaming the response.",
        }
        error_json = f"data: {json.dumps(error_data)}\n\n"
        return StreamingResponse(
            iter([error_json]),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
            },
        )
