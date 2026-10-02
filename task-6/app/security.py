"""API key check and a simple in-memory rate limiter (per client, per minute)."""
import hmac
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, limit, window=60.0, clock=time.monotonic):
        self.limit, self.window, self.clock = limit, window, clock
        self.hits = defaultdict(deque)

    def allow(self, key):
        now = self.clock()
        q = self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True


def key_ok(expected, supplied):
    """True when no key is configured, or the supplied key matches (constant time)."""
    if not expected:
        return True
    return supplied is not None and hmac.compare_digest(expected, supplied)
