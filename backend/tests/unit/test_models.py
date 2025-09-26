# Unit Tests: Data Models
# These tests MUST FAIL until implementation is complete

import datetime

import pytest
from pydantic import ValidationError

from chatwait_backend.models.chat_models import (
    ChatMessage,
    ChatStreamingRequest,
    ChatWaitRequest,
    ChatWaitResponse,
    ConnectionState,
    ConversationContext,
    MessageRole,
    StreamConnection,
    StreamEndEvent,
    StreamErrorEvent,
    StreamTokenEvent,
)


class TestChatMessage:
    """Test ChatMessage model validation and behavior."""

    def test_valid_chat_message(self):
        """Test creating a valid ChatMessage."""
        # This test will fail until the model is implemented
        message = ChatMessage(
            role=MessageRole.USER, content="Hello, world!", token_count=3
        )

        assert message.role == MessageRole.USER
        assert message.content == "Hello, world!"
        assert message.token_count == 3
        assert isinstance(message.timestamp, datetime.datetime)

    def test_invalid_role(self):
        """Test that invalid roles are rejected."""
        # This test will fail until the model is implemented
        with pytest.raises(ValidationError):
            ChatMessage(
                role="invalid_role",  # type: ignore
                content="Test message",
                token_count=2,
            )

    def test_empty_content(self):
        """Test that empty content is rejected."""
        # This test will fail until the model is implemented
        with pytest.raises(ValidationError):
            ChatMessage(
                role=MessageRole.USER,
                content="",  # Empty content
                token_count=0,
            )

    def test_content_too_long(self):
        """Test that content exceeding max length is rejected."""
        # This test will fail until the model is implemented
        long_content = "a" * 10001  # Exceeds 10000 char limit
        with pytest.raises(ValidationError):
            ChatMessage(role=MessageRole.USER, content=long_content, token_count=10001)

    def test_negative_token_count(self):
        """Test that negative token counts are rejected."""
        # This test will fail until the model is implemented
        with pytest.raises(ValidationError):
            ChatMessage(
                role=MessageRole.USER,
                content="Test message",
                token_count=-1,  # Negative token count
            )

    def test_zero_token_count(self):
        """Test that zero token counts are rejected."""
        # This test will fail until the model is implemented
        with pytest.raises(ValidationError):
            ChatMessage(
                role=MessageRole.USER,
                content="Test message",
                token_count=0,  # Zero token count
            )


class TestConversationContext:
    """Test ConversationContext model validation."""

    def test_valid_conversation_context(self):
        """Test creating a valid ConversationContext."""
        # This test will fail until the model is implemented
        context = ConversationContext(
            session_id="test-session-123", messages=[], metadata={"test": True}
        )

        assert context.session_id == "test-session-123"
        assert len(context.messages) == 0
        assert context.metadata == {"test": True}

    def test_empty_session_id(self):
        """Test that empty session IDs are rejected."""
        # This test will fail until the model is implemented
        with pytest.raises(ValidationError):
            ConversationContext(session_id="")  # Empty session ID


class TestStreamConnection:
    """Test StreamConnection model validation."""

    def test_valid_stream_connection(self):
        """Test creating a valid StreamConnection."""
        # This test will fail until the model is implemented
        connection = StreamConnection(
            event_source="test-source",
            connection_state=ConnectionState.STREAMING,
            last_token_index=5,
            context_session_id="context-123",
        )

        assert connection.event_source == "test-source"
        assert connection.connection_state == ConnectionState.STREAMING
        assert connection.last_token_index == 5
        assert connection.context_session_id == "context-123"

    def test_negative_token_index(self):
        """Test that negative token indices are rejected."""
        # This test will fail until the model is implemented
        with pytest.raises(ValidationError):
            StreamConnection(last_token_index=-1)  # Negative token index


class TestChatWaitRequest:
    """Test ChatWaitRequest model validation."""

    def test_valid_request(self):
        """Test valid chat wait request."""
        # This test will fail until the model is implemented
        request = ChatWaitRequest(message="Hello world")

        assert request.message == "Hello world"
        assert request.context_id is None

    def test_request_with_context(self):
        """Test request with optional context ID."""
        # This test will fail until the model is implemented
        request = ChatWaitRequest(message="Hello world", context_id="context-123")

        assert request.message == "Hello world"
        assert request.context_id == "context-123"


class TestChatWaitResponse:
    """Test ChatWaitResponse model validation."""

    def test_valid_response(self):
        """Test valid chat wait response."""
        # This test will fail until the model is implemented
        response = ChatWaitResponse(
            message="Hello! How can I help you?",
            context_id="context-123",
            token_count=6,
            processing_time_ms=245.5,
        )

        assert response.message == "Hello! How can I help you?"
        assert response.context_id == "context-123"
        assert response.token_count == 6
        assert response.processing_time_ms == 245.5


class TestChatStreamingRequest:
    """Test ChatStreamingRequest model validation."""

    def test_valid_streaming_request(self):
        """Test valid streaming request."""
        # This test will fail until the model is implemented
        request = ChatStreamingRequest(message="Hello streaming")

        assert request.message == "Hello streaming"
        assert request.context_id is None
        assert request.last_token_index is None

    def test_streaming_request_with_reconnection(self):
        """Test streaming request with reconnection parameters."""
        # This test will fail until the model is implemented
        request = ChatStreamingRequest(
            message="Hello streaming", context_id="context-123", last_token_index=5
        )

        assert request.message == "Hello streaming"
        assert request.context_id == "context-123"
        assert request.last_token_index == 5


class TestStreamingEvents:
    """Test streaming event models."""

    def test_stream_token_event(self):
        """Test StreamTokenEvent model."""
        # This test will fail until the model is implemented
        event = StreamTokenEvent(token="Hello", token_index=0, context_id="context-123")

        assert event.token == "Hello"
        assert event.token_index == 0
        assert event.context_id == "context-123"
        assert event.event_type == "token"

    def test_stream_end_event(self):
        """Test StreamEndEvent model."""
        # This test will fail until the model is implemented
        event = StreamEndEvent(context_id="context-123", final_output="Hello world!")

        assert event.context_id == "context-123"
        assert event.event_type == "end"
        assert event.final_output == "Hello world!"

    def test_stream_error_event(self):
        """Test StreamErrorEvent model."""
        # This test will fail until the model is implemented
        event = StreamErrorEvent(
            context_id="context-123",
            error_code="TEST_ERROR",
            message="Test error message",
        )

        assert event.context_id == "context-123"
        assert event.event_type == "error"
        assert event.error_code == "TEST_ERROR"
        assert event.message == "Test error message"
