from fastapi import APIRouter

from api.v1 import health, settings, tasks

# Main v1 router —— versioned entrypoint for all /api/v1/* endpoints
router = APIRouter(prefix="/v1", tags=["v1"])

# Register sub-routers
router.include_router(health.router, prefix="", tags=["Health"])
router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
router.include_router(settings.router, prefix="/settings", tags=["Settings"])

__all__ = ["router"]