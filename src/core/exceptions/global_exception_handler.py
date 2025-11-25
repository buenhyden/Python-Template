import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    """
    처리되지 않은 모든 예외(500 Internal Server Error)를 잡아서 처리
    """
    # 에러 스택 트레이스를 로그에 상세히 기록 (Request ID 포함됨)
    logger.error(f"Global Exception Handler Caught: {exc}")
    logger.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support.",
        },
    )
