import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions import AuditServiceError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("validation error", extra={"request_id": getattr(request.state, "request_id", "unknown")})
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error"
            },
            )

    @app.exception_handler(AuditServiceError)
    async def audit_service_error_handler(request: Request, exc: AuditServiceError):
        logger.error("service error", extra={"request_id": getattr(request.state, "request_id", "unknown"), "message": exc.message})
        return JSONResponse(status_code=exc.status_code, content=
                            {"error": "service_error", 
                             "message":exc.message})

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.warning("value error", extra={"request_id": getattr(request.state, "request_id", "unknown"), "message": str(exc)})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"error": "invalid_request",
                                      "message": str(exc)})
