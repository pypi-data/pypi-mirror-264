__all__ = ["RateLimitRetry"]

import logging
import time
from typing import Optional

try:
    # sadly mypy doesn't support `except ImportError` based checks
    from urllib3.response import BaseHTTPResponse  # type: ignore[attr-defined]
except ImportError:
    # compatability between urllib v1 and v2
    # minimum urllib3 version should be 1.26 due to Retry arguments
    # types-requests starts requiring urllib v2, which requests itself does not
    # therefore it's version locked https://github.com/python/typeshed/blob/00ec260fcb131367f2426b4a9a555c3dec28fd37/stubs/requests/METADATA.toml#L5
    # the tests should have caught this import error, but didn't because of type-requests versions
    from urllib3.response import HTTPResponse as BaseHTTPResponse
from urllib3.util.retry import Retry

from .settings import RATE_LIMIT_HEADERS
from .utils import parse_rate_limit

LOG = logging.getLogger(__name__)


class RateLimitRetry(Retry):
    """A retry strategy that honors rate-limit headers if present."""

    def get_rate_limit_header(self, response: BaseHTTPResponse) -> Optional[str]:
        """Parse a response and get the rate limit header if it exists."""
        for header in RATE_LIMIT_HEADERS:
            if header in response.headers:
                return header
        else:
            return None

    def get_rate_limit_wait(self, response: BaseHTTPResponse) -> Optional[float]:
        """
        Get the value of RateLimit header in seconds.

        RateLimit-Reset can either be a timestamp representing a point in the future when the rate limit
        resets--OR--it can be the number of seconds until the reset. There are several semi-standard rate-limiting
        headers to check for.
        """
        header_name = self.get_rate_limit_header(response)
        if not header_name:
            return None

        limit_value = response.getheader(header_name)
        if limit_value:
            try:
                limit_float = float(limit_value)
            except ValueError:
                LOG.error("Header `%s` value `%s` is not a valid number", header_name, limit_value)
                return None
            return parse_rate_limit(limit_float)
        else:
            return None

    def sleep_for_ratelimit(self, response: BaseHTTPResponse) -> bool:
        wait = self.get_rate_limit_wait(response)
        if wait:
            LOG.debug("Sleeping for %s seconds as requested by Rate-Limit header", wait)
            time.sleep(wait)
            return True
        return False

    def sleep(self, response: Optional[BaseHTTPResponse] = None) -> None:
        """
        Sleep between retry attempts.

        If there are rate-limit headers present then these are honored.
        """
        if response and self.get_rate_limit_header(response):
            did_sleep = self.sleep_for_ratelimit(response)
            if did_sleep:
                return
        super().sleep(response=response)
