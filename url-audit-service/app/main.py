import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.audit import analyze_url_async
from app.config import settings
from app.dependencies import cache, enforce_rate_limit, managed_audit_context
from app.errors import register_exception_handlers
from app.logger import configure_logging
from app.middleware import add_request_id_middleware
from app.schemas import AuditRequest, AuditResponse

logger = logging.getLogger(__name__)

configure_logging()
app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://url-audit-service-frontend-4x7e5vkdl-muskan090s-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_request_id_middleware(app)
register_exception_handlers(app)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/audit", response_model=AuditResponse)
async def audit_url(request: Request, payload: AuditRequest, _: None = Depends(enforce_rate_limit)) -> AuditResponse:
    logger.info("audit requested", extra={"request_id": getattr(request.state, "request_id", "unknown"), "url": payload.url})
    cached = cache.get(payload.url)
    if cached is not None:
        logger.info("cache hit", extra={"request_id": getattr(request.state, "request_id", "unknown"), "url": payload.url})
        return AuditResponse(url=payload.url, result=cached)

    async with managed_audit_context():
        try:
            result = await analyze_url_async(payload.url, settings.request_timeout_seconds)
        except TimeoutError:
            logger.warning("audit timed out", extra={"request_id": getattr(request.state, "request_id", "unknown"), "url": payload.url})
            raise

    cache.set(payload.url, result)
    logger.info("audit completed", extra={"request_id": getattr(request.state, "request_id", "unknown"), "url": payload.url, "result": result})
    return AuditResponse(url=payload.url, result=result)
