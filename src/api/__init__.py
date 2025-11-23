from fastapi import APIRouter

from src.api.status import router as status_router

router = APIRouter()

router.include_router(status_router, tags=["Health"])
