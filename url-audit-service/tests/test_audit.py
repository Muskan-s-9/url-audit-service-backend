import pytest

from app.audit import analyze_url, analyze_url_async


@pytest.mark.asyncio
async def test_analyze_url_accepts_valid_https_url():
    result = analyze_url("https://example.com")
    assert result["is_valid"] is True
    assert result["domain"] == "example.com"


def test_analyze_url_rejects_invalid_url():
    result = analyze_url("not-a-url")
    assert result["is_valid"] is False
    assert result["domain"] == ""


@pytest.mark.asyncio
async def test_analyze_url_async_returns_result():
    result = await analyze_url_async("https://example.org", timeout_seconds=5.0)
    assert result["is_valid"] is True
    assert result["domain"] == "example.org"
