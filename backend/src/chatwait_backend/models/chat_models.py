"""Pydantic models for ChatWait entities.

These models define the data structures used in API requests and responses,
aligned with OpenAI Agents SDK schema for maximum compatibility.
"""

import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MessageRole(str, Enum):
    """OpenAI compatible message roles."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Represents a single chat message using OpenAI ChatMessage format.

    This model aligns with OpenAI's standard message format for maximum
    compatibility with the Agents SDK.
    """

    role: MessageRole = Field(..., description="Message role (user/assistant/system)")
    content: str = Field(
        ..., description="Message content", min_length=1, max_length=10000
    )
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="When the message was created",
    )
    token_count: int = Field(..., description="Number of tokens in the message", gt=0)

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v):
        """Ensure role is valid OpenAI role."""
        if isinstance(v, str):
            v = v.lower()
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        """Ensure content is not empty and within limits."""
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        if len(v) > 10000:
            raise ValueError(
                "Message content exceeds maximum length of 10000 characters"
            )
        return v.strip()


class ConversationContext(BaseModel):
    """Represents conversation context using OpenAI AgentSession structure.

    This model leverages the OpenAI Agents SDK's built-in session management
    for conversation state and history.
    """

    session_id: str = Field(..., description="Unique session identifier")
    messages: list[ChatMessage] = Field(
        default_factory=list, description="Conversation message history"
    )
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="When the session was initiated",
    )
    last_updated: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="When the session was last modified",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional session metadata for extensibility",
    )

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v):
        """Ensure session_id is not empty."""
        if not v or not v.strip():
            raise ValueError("Session ID cannot be empty")
        return v.strip()


class ConnectionState(str, Enum):
    """Streaming connection states."""

    CONNECTING = "connecting"
    STREAMING = "streaming"
    RECONNECTING = "reconnecting"
    TERMINATED = "terminated"


class StreamConnection(BaseModel):
    """Custom wrapper for streaming connections with reconnection support.

    This model extends the OpenAI Agents SDK's streaming capabilities
    with custom reconnection support and state management.
    """

    event_source: str | None = Field(
        None, description="Server-sent event source identifier"
    )
    connection_state: ConnectionState = Field(
        default=ConnectionState.CONNECTING, description="Current connection state"
    )
    last_token_index: int = Field(
        default=0, description="Last successfully delivered token index for resumption"
    )
    context_session_id: str | None = Field(
        None, description="Reference to conversation context session"
    )
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="When the connection was established",
    )
    last_activity: datetime.datetime = Field(
        default_factory=datetime.datetime.now, description="Last activity timestamp"
    )

    @field_validator("last_token_index")
    @classmethod
    def validate_token_index(cls, v):
        """Ensure token index is non-negative."""
        if v < 0:
            raise ValueError("Token index cannot be negative")
        return v


# Request/Response models for API endpoints
class ChatWaitRequest(BaseModel):
    """Request model for /chat/wait endpoint."""

    message: str = Field(
        ..., description="User message", min_length=1, max_length=10000
    )
    context_id: str | None = Field(
        None, description="Optional context ID for conversation continuity"
    )


class ChatWaitResponse(BaseModel):
    """Response model for /chat/wait endpoint."""

    message: str = Field(..., description="Assistant response")
    context_id: str = Field(..., description="Context ID for this conversation")
    token_count: int = Field(..., description="Number of tokens in response", gt=0)
    processing_time_ms: float = Field(
        ..., description="Processing time in milliseconds", ge=0
    )


class ChatStreamingRequest(BaseModel):
    """Request model for /chat/streaming endpoint."""

    message: str = Field(
        ..., description="User message", min_length=1, max_length=10000
    )
    context_id: str | None = Field(
        None, description="Optional context ID for conversation continuity"
    )
    last_token_index: int | None = Field(
        None, description="Resume from this token index", ge=0
    )


class StreamTokenEvent(BaseModel):
    """SSE event for streaming tokens."""

    token: str = Field(..., description="Response token")
    token_index: int = Field(..., description="Sequential token index", ge=0)
    context_id: str = Field(..., description="Context ID for conversation")
    event_type: str = Field(default="token", description="Event type")


class StreamEndEvent(BaseModel):
    """SSE event for stream completion."""

    context_id: str = Field(..., description="Context ID for conversation")
    event_type: str = Field(default="end", description="Event type")
    final_output: str = Field(..., description="Complete final response")


class StreamErrorEvent(BaseModel):
    """SSE event for streaming errors."""

    context_id: str | None = Field(None, description="Context ID for conversation")
    event_type: str = Field(default="error", description="Event type")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
