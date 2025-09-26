# Contract Test: Error handling
# These tests MUST FAIL until implementation is complete

import pytest
from fastapi.testclient import TestClient

from chatwait_backend.app import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


def test_error_response_format(client):
    """Test that all error responses follow consistent JSON format."""
    # Test missing message error
    response = client.post("/api/v1/chat/wait", json={})

    # FastAPI returns 422 for Pydantic validation errors
    assert response.status_code == 422
    data = response.json()

    # Validate error response structure (FastAPI/Pydantic format)
    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0

    # Check that the error mentions the missing message field
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0

    # Should not contain internal implementation details
    assert "stack" not in data
    assert "traceback" not in data
    assert "exception" not in data


def test_different_error_types(client):
    """Test different types of errors return appropriate codes and messages."""
    # Test empty message
    response = client.post("/api/v1/chat/wait", json={"message": ""})
    assert response.status_code == 422  # FastAPI validation error
    data = response.json()
    # Check that the error mentions the message field validation
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0

    # Test message too long (simulate)
    long_message = "a" * 10001  # Assuming 10000 char limit
    response = client.post("/api/v1/chat/wait", json={"message": long_message})
    assert response.status_code == 422  # FastAPI validation error
    data = response.json()
    # Check that the error mentions the message field validation
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0


def test_streaming_error_handling(client):
    """Test error handling in streaming endpoints."""
    # Test missing message in streaming
    response = client.get("/api/v1/chat/streaming")
    assert (
        response.status_code == 422
    )  # FastAPI validation error for missing required query param
    data = response.json()
    assert "detail" in data
    # Check that the error mentions the message parameter
    message_errors = [error for error in data["detail"] if "message" in str(error)]
    assert len(message_errors) > 0


def test_nonexistent_endpoint(client):
    """Test 404 errors for non-existent endpoints."""
    response = client.post("/api/v1/nonexistent", json={"message": "test"})
    assert response.status_code == 404

    # Should still follow error format if middleware is implemented
    try:
        data = response.json()
        if "error_code" in data:
            assert "NOT_FOUND" in data["error_code"]
    except Exception:
        # If no JSON response, that's also acceptable for 404
        pass


def test_malformed_json(client):
    """Test malformed JSON request handling."""
    # Send invalid JSON
    response = client.post(
        "/api/v1/chat/wait",
        data="invalid json{",
        headers={"Content-Type": "application/json"},
    )

    # FastAPI returns 422 for malformed JSON that can't be parsed
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    # Check that the error mentions JSON parsing issues
    assert any(
        "json" in str(error).lower() or "parse" in str(error).lower()
        for error in data["detail"]
    )
