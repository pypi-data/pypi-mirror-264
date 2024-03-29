import logging
from pathlib import Path
from urllib.parse import urlparse

import requests
import urllib3
from apistar.exceptions import ErrorResponse
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
)

from arkindex import ArkindexClient, options_from_env

logger = logging.getLogger(__name__)


def should_verify_cert(url: str) -> bool:
    """
    Skip SSL certification validation when hitting a development instance
    """
    if not url:
        return True

    host = urlparse(url).netloc
    return not host.endswith("ark.localhost")


def _get_arkindex_client() -> ArkindexClient:
    options = options_from_env()

    # Skip SSL verification in Arkindex API client for local development hosts
    verify = should_verify_cert(options.get("base_url"))
    if not verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.warn("SSL certificate verification is disabled for Arkindex API calls")

    return ArkindexClient(verify=verify, **options)


DEFAULT_CLIENT = _get_arkindex_client()


def _is_500_error(exc: Exception) -> bool:
    """
    Check if an Arkindex API error is a 50x
    This is used to retry most API calls implemented here
    """
    if not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.status_code < 600


@retry(
    retry=retry_if_exception(_is_500_error),
    wait=wait_exponential(multiplier=2, min=3),
    reraise=True,
    stop=stop_after_attempt(5),
    before_sleep=before_sleep_log(logger, logging.INFO),
)
def retried_request(*args, **kwargs):
    """
    Proxy all Arkindex API requests with a retry mechanism
    in case of 50X errors
    The same API call will be retried 5 times, with an exponential sleep time
    going through 3, 4, 8 and 16 seconds of wait between call.
    If the 5th call still gives a 50x, the exception is re-raised
    and the caller should catch it
    Log messages are displayed before sleeping (when at least one exception occurred)
    """
    return DEFAULT_CLIENT.request(*args, **kwargs)


# Time to wait before retrying the IIIF image information fetching
HTTP_GET_RETRY_BACKOFF = 10

DOWNLOAD_CHUNK_SIZE = 8192


@retry(
    reraise=True,
    retry=retry_if_exception_type(requests.RequestException),
    stop=stop_after_attempt(3),
    wait=wait_fixed(HTTP_GET_RETRY_BACKOFF),
)
def download_file(url: str, path: Path) -> None:
    """
    Download a URL into a local path, retrying if necessary
    """
    with requests.get(url, stream=True, verify=should_verify_cert(url)) as r:
        r.raise_for_status()
        with path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                if chunk:  # Ignore empty chunks
                    f.write(chunk)
