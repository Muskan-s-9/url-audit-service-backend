import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, HTTPException, Request

from app.cache import InMemoryCache
from app.config import settings
from app.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

cache = InMemoryCache(max_size=settings.cache_max_items, ttl_seconds=settings.cache_ttl_seconds)
rate_limiter = RateLimiter(max_requests=settings.rate_limit_requests, window_seconds=settings.rate_limit_window_seconds)

_semaphore = asyncio.Semaphore(settings.max_concurrency)


async def enforce_rate_limit(request: Request) -> None:
    client_key = request.headers.get("x-forwarded-for") or request.client.host if request.client else "unknown"
    if not rate_limiter.allow(client_key):
        logger.warning("rate limit exceeded", extra={"request_id": getattr(request.state, "request_id", "unknown"), "client": client_key})
        raise HTTPException(status_code=429, detail={"error": "rate_limit_exceeded", "message": "Too many requests"})


async def enforce_concurrency() -> None:
    await _semaphore.acquire()


async def release_concurrency() -> None:
    _semaphore.release()


@asynccontextmanager
async def managed_audit_context() -> AsyncIterator[None]:
    await enforce_concurrency()
    try:
        yield
    finally:
        await release_concurrency()
