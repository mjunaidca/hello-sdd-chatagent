"""Main entry point for ChatWait backend API server.

This module starts the FastAPI server with uvicorn for testing and development.
"""

import uvicorn

from chatwait_backend.config import settings


def main():
    """Start the FastAPI server."""
    print("🚀 Starting ChatWait API server...")
    print(f"📍 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"📚 API Documentation: http://{settings.host}:{settings.port}/docs")
    print(f"🔄 Health Check: http://{settings.host}:{settings.port}/health")
    print(f"💬 Chat Endpoints: http://{settings.host}:{settings.port}/api/v1/chat/wait")
    print(f"📡 Streaming: http://{settings.host}:{settings.port}/api/v1/chat/streaming")
    print(f"⚙️  Debug mode: {settings.debug}")

    uvicorn.run(
        "chatwait_backend.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
