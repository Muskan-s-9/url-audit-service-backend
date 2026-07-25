def normalize_url(url: str) -> str:
    return url.strip().rstrip("/") if url else ""
