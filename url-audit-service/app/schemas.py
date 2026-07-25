from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator


class AuditRequest(BaseModel):
    url: str = Field(..., min_length=1)

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("URL must be a string")

        normalized = value.strip()
        if not normalized:
            raise ValueError("URL must not be empty")

        parsed = urlparse(normalized)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("URL must be a valid http/https URL")

        return normalized


class AuditResponse(BaseModel):
    url: str
    result: dict[str, object]
