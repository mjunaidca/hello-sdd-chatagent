# Contract Test: /chat/wait endpoint
# These tests MUST FAIL until implementation is complete

import time

import pytest
from fastapi.testclient import TestClient

from chatwait_backend.app import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


def test_chat_wait_valid_request(client):
    """Test /chat/wait with valid input should return successful response."""
    # This test will fail until the endpoint is implemented
    response = client.post("/api/v1/chat/wait", json={"message": "Hello, how are you?"})

    # Should return 200 with proper response structure
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "context_id" in data
    assert "token_count" in data
    assert "processing_time_ms" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0


def test_chat_wait_missing_message(client):
    """Test /chat/wait with missing message should return 422 validation error."""
    # FastAPI automatically validates Pydantic models and returns 422 for missing required fields
    response = client.post("/api/v1/chat/wait", json={})

    # Should return 422 with validation error structure
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    # Check that the error mentions the missing message field
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0


def test_chat_wait_empty_message(client):
    """Test /chat/wait with empty message should return 422 validation error."""
    # FastAPI automatically validates Pydantic models and returns 422 for invalid field values
    response = client.post("/api/v1/chat/wait", json={"message": ""})

    # Should return 422 with validation error structure
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    # Check that the error mentions the message field validation
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0


def test_chat_wait_response_format(client):
    """Test /chat/wait response follows required JSON schema."""
    # This test will fail until the endpoint is implemented
    response = client.post("/api/v1/chat/wait", json={"message": "Test message"})

    # Should return 200 with proper response structure
    assert response.status_code == 200
    data = response.json()

    # Validate response structure
    required_fields = ["message", "context_id", "token_count", "processing_time_ms"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Validate field types
    assert isinstance(data["message"], str)
    assert isinstance(data["context_id"], str)
    assert isinstance(data["token_count"], int)
    assert isinstance(data["processing_time_ms"], (int, float))

    # Validate business rules
    assert len(data["message"]) > 0
    assert data["token_count"] > 0
    assert data["processing_time_ms"] >= 0


def test_chat_wait_performance(client):
    """Test /chat/wait response time meets performance requirements."""
    # This test will fail until the endpoint is implemented
    start_time = time.time()

    response = client.post("/api/v1/chat/wait", json={"message": "Performance test"})

    end_time = time.time()
    response_time_ms = (end_time - start_time) * 1000

    # Should return 200 within performance requirements
    assert response.status_code == 200
    assert (
        response_time_ms < 5000
    ), f"Response too slow: {response_time_ms}ms (max 5000ms allowed)"
