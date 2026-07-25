from app.rate_limiter import RateLimiter


def test_rate_limiter_allows_requests_under_limit():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("user") is True
    assert limiter.allow("user") is True


def test_rate_limiter_blocks_requests_over_limit():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    assert limiter.allow("user") is True
    assert limiter.allow("user") is False


def test_rate_limiter_reset_clears_state():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    assert limiter.allow("user") is True
    limiter.reset("user")
    assert limiter.allow("user") is True
