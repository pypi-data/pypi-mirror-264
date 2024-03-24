POOL_CONNECTIONS: int = 10
"""The number of connection pools to cache."""

POOL_MAXSIZE: int = 10
"""Max connections to a host for a connection pool. (Only matters for concurrency)."""

REQUESTS_TIMEOUT: int = 60
"""Default timeout for connection attempts."""

RETRIES: int = 4
"""Number of attempts to retry connection failures."""

RETRY_BACKOFF: float = 1.0
"""
Default backoff factor for retries.

The requests library uses `b * (2 ** (i - 1))` where b is the backoff factor (this value) and i is the retry
number.
"""

RETRY_STATUS_CODES: list[int] = [
    408,  # Request timeout
    429,  # Too many requests
    502,  # Bad gateway
    503,  # Service unavailable
    504,  # Gateway timeout
]
"""TaskStatus codes which should trigger a retry attempt."""

RATE_LIMIT_HEADERS: tuple[str, ...] = ("X-RateLimit-Reset", "RateLimit-Reset", "X-Rate-Limit-Reset")
"""Common header names that indicate when a rate limited endpoint will reset."""
