from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Error: {exc}")
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(f"Validation Error: {exc}")
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
