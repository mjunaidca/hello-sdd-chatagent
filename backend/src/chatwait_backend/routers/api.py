"""API router for ChatWait endpoints."""

from fastapi import APIRouter

from chatwait_backend.api.health import router as health_router
from chatwait_backend.routers.chat import router as chat_router

router = APIRouter(prefix="", tags=["api"])

# Include health endpoints
router.include_router(health_router, prefix="", tags=["health"])

# Include chat endpoints
router.include_router(chat_router, prefix="/chat", tags=["chat"])
