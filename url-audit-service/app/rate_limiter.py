import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        timestamps = self._history[key]
        timestamps[:] = [ts for ts in timestamps if now - ts < self.window_seconds]
        if len(timestamps) >= self.max_requests:
            return False
        timestamps.append(now)
        return True

    def reset(self, key: str | None = None) -> None:
        if key is None:
            self._history.clear()
        else:
            self._history.pop(key, None)
