from app.cache import InMemoryCache
import time

def test_cache_stores_and_retrieves_values():
    cache = InMemoryCache(max_size=2, ttl_seconds=60)
    cache.set("a", {"value": 1})
    assert cache.get("a") == {"value": 1}


def test_cache_evicts_oldest_entry_when_full():
    cache = InMemoryCache(max_size=2, ttl_seconds=60)
    cache.set("a", {"value": 1})
    cache.set("b", {"value": 2})
    cache.set("c", {"value": 3})
    assert cache.get("a") is None
    assert cache.get("b") == {"value": 2}

def test_cache_updates_lru_order():
    cache = InMemoryCache(max_size=2, ttl_seconds=60)

    cache.set("a", {"value": 1})
    cache.set("b", {"value": 2})

    # Make "a" the most recently used
    cache.get("a")

    cache.set("c", {"value": 3})

    assert cache.get("b") is None
    assert cache.get("a") == {"value": 1}
    assert cache.get("c") == {"value": 3}



def test_cache_expires_entries():
    cache = InMemoryCache(max_size=2, ttl_seconds=1)

    cache.set("a", {"value": 1})

    time.sleep(1.1)

    assert cache.get("a") is None
