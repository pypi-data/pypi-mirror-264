__all__ = ["ExtendedSession", "retry_strategy", "timeout_adapter", "get_session"]

import logging
import time
from typing import Optional, Union

from requests import Session

from .hooks import log_response_errors
from .http_adapter import TimeoutHTTPAdapter
from .retry import RateLimitRetry
from .settings import POOL_CONNECTIONS, POOL_MAXSIZE, RATE_LIMIT_HEADERS, RETRIES, RETRY_BACKOFF, RETRY_STATUS_CODES
from .utils import parse_rate_limit

LOG = logging.getLogger(__name__)


class ExtendedSession(Session):
    @staticmethod
    def _has_retry_text(value: Optional[str]) -> bool:
        """
        Check for the presence of known response text that correlates with a rate limit error.

        Rate limit headers are used in most cases by most API's but in some cases the headers aren't always present for
        rate limit errors that occur during an authentication attempt. This text captures a case known to Auth0 and
        github under certain circumstances; we use it to determine if an API is failing authentication due to rate
        limiting without setting the rate-limit or x-rate-limit header.
        """
        try:
            return "please try again in a bit" in value
        except (TypeError, ValueError):
            return False

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        """
        Dispatch requests with special handling for rate-limited auth endpoints.

        For 401 errors, sometimes rate-limiting is at play. If rate-limit headers are present, honor their
        wait times. For other endpoints response text is sometimes used to indicate rate limiting, in known
        cases, fallback to a retry strategy for the request.
        """
        kwargs = {
            "params": params,
            "data": data,
            "headers": headers,
            "cookies": cookies,
            "files": files,
            "auth": auth,
            "timeout": timeout,
            "allow_redirects": allow_redirects,
            "proxies": proxies,
            "hooks": hooks,
            "stream": stream,
            "verify": verify,
            "cert": cert,
            "json": json,
        }
        if method.upper() != "POST":
            return super().request(method, url, **kwargs)

        response = super().request(method, url, **kwargs)
        if response.status_code != 401:
            return response

        # If there were any rate-limit headers, parse them and wait the appropriate time then try again.
        response_headers = response.headers
        rate_gen = (response_headers.get(x) for x in RATE_LIMIT_HEADERS)
        rate_limit: Union[str, int, None] = next((x for x in rate_gen if x), None)

        if rate_limit:
            try:
                converted_rate_limit = float(rate_limit)
            except (ValueError, TypeError):
                LOG.warning("Ignored invalid rate limit value: `%s`", rate_limit)
                return response
            else:
                wait = parse_rate_limit(converted_rate_limit)
                LOG.debug("Sleeping for %s seconds to honor Rate-Limit headers", wait)
                time.sleep(wait)
                return super().request(method, url, **kwargs)

        if self._has_retry_text(response.text):
            for i in range(RETRIES):
                wait = 0.5 * (2 ** (i - 1))
                time.sleep(wait)
                LOG.debug("Sleeping for %s seconds to retry authentication.", wait)
                response = super().request(method, url, **kwargs)
                if response.status_code != 401:
                    return response
                else:
                    if self._has_retry_text(response.text):
                        continue
                    else:
                        return response
            else:
                return super().request(method, url, **kwargs)
        else:
            return super().request(method, url, **kwargs)


# Setup a reasonable retry strategy
retry_strategy = RateLimitRetry(
    total=RETRIES,
    backoff_factor=RETRY_BACKOFF,
    status_forcelist=RETRY_STATUS_CODES,
    allowed_methods=["HEAD", "GET", "PUT", "POST", "PATCH", "DELETE", "TRACE"],
)

# Create a global DefaultHTTPAdapter to allow connection pooling for cases where concurrent requests are dispatched;
# also automatically include a default timeout.
timeout_adapter = TimeoutHTTPAdapter(
    pool_connections=POOL_CONNECTIONS,
    pool_maxsize=POOL_MAXSIZE,
    max_retries=retry_strategy,
)


def get_session() -> ExtendedSession:
    """Create a requests Session with a retry strategy and timeout set suitable for production use."""
    session = ExtendedSession()
    session.mount("http://", timeout_adapter)
    session.mount("https://", timeout_adapter)
    session.hooks["response"] = [log_response_errors]
    return session
