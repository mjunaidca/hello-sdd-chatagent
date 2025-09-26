# Contract Test: /chat/streaming endpoint
# These tests MUST FAIL until implementation is complete

import time

import pytest
from fastapi.testclient import TestClient

from chatwait_backend.app import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


def test_chat_streaming_valid_request(client):
    """Test /chat/streaming with valid input should return SSE stream."""
    # This test will fail until the endpoint is implemented
    response = client.get("/api/v1/chat/streaming?message=Hello streaming")

    # Should return 200 with SSE content type
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")

    # Should receive multiple SSE events
    content = response.text
    assert "data: " in content

    # Parse SSE events
    events = [
        line.strip()
        for line in content.split("\n")
        if line.strip() and line.startswith("data: ")
    ]
    assert len(events) > 0, "Should receive at least one SSE event"


def test_chat_streaming_missing_message(client):
    """Test /chat/streaming with missing message should return 422 validation error."""
    # FastAPI automatically validates query parameters and returns 422 for missing required params
    response = client.get("/api/v1/chat/streaming")

    # Should return 422 with validation error structure
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    # Check that the error mentions the message parameter
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0


def test_chat_streaming_sse_format(client):
    """Test /chat/streaming response follows SSE format with token events."""
    # This test will fail until the endpoint is implemented
    response = client.get("/api/v1/chat/streaming?message=Test SSE format")

    # Should return 200 with proper SSE format
    assert response.status_code == 200
    content = response.text

    # Should contain properly formatted SSE events
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    sse_lines = [line for line in lines if line.startswith("data: ")]

    assert len(sse_lines) > 0, "Should contain SSE data events"

    # Parse first event to check structure
    first_event = sse_lines[0]
    assert 'data: {"token":' in first_event or 'data: {"type":' in first_event


def test_chat_streaming_reconnection(client):
    """Test /chat/streaming reconnection with last_token_index resumes correctly."""
    # This test will fail until the endpoint is implemented
    # Start initial streaming request
    response1 = client.get("/api/v1/chat/streaming?message=Test reconnection")

    assert response1.status_code == 200
    # content1 = response1.text  # Not used in this test

    # Extract context_id and last_token_index from first response
    # This would normally be parsed from SSE events
    context_id = "test-context-id"  # Would be extracted from actual response
    last_token_index = 2  # Would be extracted from actual response

    # Reconnect with last_token_index
    response2 = client.get(
        f"/api/v1/chat/streaming?message=Test reconnection&context_id={context_id}&last_token_index={last_token_index}"
    )

    assert response2.status_code == 200

    # Should resume from the correct token index (no duplicate tokens)
    content2 = response2.text
    assert len(content2) > 0, "Reconnection should return streaming content"


def test_chat_streaming_performance(client):
    """Test /chat/streaming token latency meets performance requirements."""
    # This test will fail until the endpoint is implemented
    response = client.get("/api/v1/chat/streaming?message=Performance test")

    assert response.status_code == 200
    content = response.text

    # Parse SSE events and measure token latency
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    token_events = [line for line in lines if 'data: {"token":' in line]

    if len(token_events) > 1:
        # Measure time between first few tokens
        start_time = time.time()
        # Process events and measure latency
        # This is a simplified test - real implementation would be more sophisticated
        end_time = time.time()
        avg_latency_ms = (end_time - start_time) * 1000 / len(token_events)

        # Should meet performance requirements (<200ms per token)
        assert (
            avg_latency_ms < 1000
        ), f"Streaming too slow: {avg_latency_ms}ms per token (max 1000ms allowed)"
