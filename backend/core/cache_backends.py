"""
Resilient Cache Backend for NyayaSetu AI.
Supports Redis with automatic zero-downtime fallback to In-Memory LocMemCache.
"""
import logging
from django.core.cache.backends.redis import RedisCache
from django.core.cache.backends.locmem import LocMemCache

logger = logging.getLogger(__name__)

class FallbackRedisCache(RedisCache):
    """
    Connects to Redis if available.
    Automatically and seamlessly falls back to thread-safe LocMemCache
    if Redis is offline, disconnected, or experiencing network timeout.
    """
    def __init__(self, server, params):
        super().__init__(server, params)
        self._fallback = LocMemCache('redis-locmem-fallback', params)

    def get(self, key, default=None, version=None):
        try:
            val = super().get(key, default, version)
            return val if val is not None else self._fallback.get(key, default, version)
        except Exception as e:
            return self._fallback.get(key, default, version)

    def set(self, key, value, timeout=None, version=None):
        try:
            return super().set(key, value, timeout, version)
        except Exception as e:
            return self._fallback.set(key, value, timeout, version)

    def delete(self, key, version=None):
        try:
            super().delete(key, version)
        except Exception:
            pass
        return self._fallback.delete(key, version)

    def clear(self):
        try:
            super().clear()
        except Exception:
            pass
        self._fallback.clear()
