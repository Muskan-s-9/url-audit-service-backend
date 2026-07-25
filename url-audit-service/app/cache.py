import time
from collections import OrderedDict


class InMemoryCache:
    def __init__(self, max_size: int = 100, ttl_seconds: int = 300) -> None:
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._store: OrderedDict[str, dict[str, object]] = OrderedDict()

    def _purge_expired(self) -> None:
        now = time.monotonic()
        expired_keys = [key for key, entry in self._store.items() if now >= entry["expires_at"]]
        for key in expired_keys:
            self._store.pop(key, None)

    def get(self, key: str) -> dict | None:
        self._purge_expired()
        if key in self._store:
            self._store.move_to_end(key)
            return self._store[key]["value"]
        return None

    def set(self, key: str, value: dict) -> None:
        self._purge_expired()
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = {"value": value, "expires_at": time.monotonic() + self.ttl_seconds}
        if len(self._store) > self.max_size:
            self._store.popitem(last=False)

    def clear(self) -> None:
        self._store.clear()
