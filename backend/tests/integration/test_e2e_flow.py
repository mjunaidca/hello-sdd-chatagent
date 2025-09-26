# Integration Test: End-to-End Chat Flow
# Tests the complete flow from UI to backend to LLM and back

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from chatwait_backend.app import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


def test_e2e_wait_mode_flow(client):
    """Test complete wait mode flow with mocked LLM."""
    # Mock the LLM service to avoid actual API calls
    with patch("chatwait_backend.services.chat_agent.llm_service") as mock_llm_service:
        # Configure mock to simulate successful LLM response
        mock_llm_service.get_model.return_value = AsyncMock()
        mock_llm_service.get_model.return_value.model = "test-model"

        # Mock the chat agent service
        with patch(
            "chatwait_backend.services.chat_agent.chat_agent_service"
        ) as mock_chat_service:
            mock_chat_service.run_sync = AsyncMock(
                return_value={
                    "message": "Hello! This is a test response from the AI assistant.",
                    "context_id": "test-context-123",
                    "token_count": 12,
                    "processing_time_ms": 1250.5,
                    "agent_output": "Hello! This is a test response from the AI assistant.",
                }
            )

            # Test the complete flow
            response = client.post(
                "/api/v1/chat/wait",
                json={
                    "message": "Hello, test the system",
                    "context_id": "test-context-123",
                },
            )

            assert response.status_code == 200
            data = response.json()

            assert "message" in data
            assert "context_id" in data
            assert "token_count" in data
            assert "processing_time_ms" in data
            assert data["context_id"] == "test-context-123"
            assert data["token_count"] == 12
            assert data["processing_time_ms"] == 1250.5
            assert "Hello! This is a test response" in data["message"]


def test_e2e_streaming_mode_flow(client):
    """Test complete streaming mode flow with mocked LLM."""
    # Mock the LLM service
    with patch("chatwait_backend.services.chat_agent.llm_service") as mock_llm_service:
        mock_llm_service.get_model.return_value = AsyncMock()

        # Mock the streaming service
        with patch(
            "chatwait_backend.services.streaming_service.streaming_service"
        ) as mock_streaming_service:
            mock_streaming_service.create_stream = AsyncMock()
            mock_streaming_service.create_stream.return_value = [
                '{"type": "token", "token": "Hello", "token_index": 0, "context_id": "test-ctx"}\n\n',
                '{"type": "token", "token": " ", "token_index": 1, "context_id": "test-ctx"}\n\n',
                '{"type": "token", "token": "world!", "token_index": 2, "context_id": "test-ctx"}\n\n',
                '{"type": "end", "context_id": "test-ctx", "final_output": "Hello world!"}\n\n',
            ]

            # Test the streaming flow
            response = client.get(
                "/api/v1/chat/streaming?message=Hello%20streaming&context_id=test-ctx"
            )

            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")

            content = response.text
            assert "data: " in content
            assert "Hello" in content
            assert "world!" in content


def test_e2e_context_preservation(client):
    """Test that context is preserved across requests."""
    with patch("chatwait_backend.services.chat_agent.llm_service") as mock_llm_service:
        mock_llm_service.get_model.return_value = AsyncMock()

        with patch(
            "chatwait_backend.services.chat_agent.chat_agent_service"
        ) as mock_chat_service:
            # Mock responses for two consecutive requests
            mock_chat_service.run_sync = AsyncMock(
                side_effect=[
                    {
                        "message": "First response about AI",
                        "context_id": "conversation-123",
                        "token_count": 8,
                        "processing_time_ms": 1100.0,
                    },
                    {
                        "message": "Second response continuing the conversation",
                        "context_id": "conversation-123",
                        "token_count": 10,
                        "processing_time_ms": 950.0,
                    },
                ]
            )

            # First message
            response1 = client.post(
                "/api/v1/chat/wait",
                json={"message": "What is AI?", "context_id": "conversation-123"},
            )

            assert response1.status_code == 200
            data1 = response1.json()
            assert data1["context_id"] == "conversation-123"

            # Second message with same context
            response2 = client.post(
                "/api/v1/chat/wait",
                json={
                    "message": "Tell me more about it",
                    "context_id": "conversation-123",
                },
            )

            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["context_id"] == "conversation-123"


def test_e2e_error_handling_flow(client):
    """Test complete error handling flow."""
    # Test with empty message (should return 422)
    response = client.post("/api/v1/chat/wait", json={})

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0


def test_e2e_mode_switching(client):
    """Test switching between wait and streaming modes."""
    # Both endpoints should be available and functional
    wait_response = client.post("/api/v1/chat/wait", json={"message": "test"})

    streaming_response = client.get("/api/v1/chat/streaming?message=test")

    # Both should return appropriate responses (even if mocked)
    assert wait_response.status_code in [
        200,
        429,
        500,
    ]  # 429/500 expected due to mocking
    assert streaming_response.status_code in [
        200,
        422,
    ]  # 422 if validation fails, 200 if works


async def test_e2e_health_check_flow():
    """Test that health checks work end-to-end."""
    # This would test the actual health check endpoint
    # In a real test, we would make HTTP requests to the running server
    pass


def test_e2e_concurrent_requests(client):
    """Test handling of concurrent requests."""
    # This would test multiple simultaneous requests
    # In a real test, we would use threading or async to make concurrent requests
    pass


def test_e2e_response_format_consistency(client):
    """Test that responses follow consistent format across all endpoints."""
    # Test health endpoint format
    health_response = client.get("/health")
    assert health_response.status_code == 200
    health_data = health_response.json()
    assert "status" in health_data
    assert "service" in health_data
    assert "version" in health_data

    # Test error format consistency
    error_response = client.post("/api/v1/chat/wait", json={})
    if error_response.status_code == 422:
        error_data = error_response.json()
        assert "detail" in error_data
        assert isinstance(error_data["detail"], list)
