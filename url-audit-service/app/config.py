import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "url-audit-service")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "5"))
    rate_limit_window_seconds: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    cache_max_items: int = int(os.getenv("CACHE_MAX_ITEMS", "200"))
    max_concurrency: int = int(os.getenv("MAX_CONCURRENCY", "10"))
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "5.0"))


settings = Settings()
