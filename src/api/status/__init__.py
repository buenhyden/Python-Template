from fastapi import APIRouter

from src.api.status.health_check import router as health_router

router = APIRouter()

router.include_router(health_router, tags=["Health"])
