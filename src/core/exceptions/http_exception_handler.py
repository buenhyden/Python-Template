import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTPException은 의도된 에러이므로 Warning 레벨로 로깅하거나 생략 가능
    """
    logger.warning(f"HTTP Exception: {exc.detail} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
