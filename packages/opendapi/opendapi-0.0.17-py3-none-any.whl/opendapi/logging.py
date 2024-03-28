"""Debugging utilities for OpenDAPI"""
import time
from enum import Enum
from importlib.metadata import version
from urllib.parse import urljoin

import requests
import sentry_sdk
from deepmerge import always_merger

DAPI_API_KEY_HEADER = "X-DAPI-Server-API-Key"
WOVEN_DENY_LIST = sentry_sdk.scrubber.DEFAULT_DENYLIST + [DAPI_API_KEY_HEADER]


class LogDistKey(Enum):
    """Set of Dist keys for logging"""

    ASK_DAPI_SERVER = "ask_dapi_server"
    CLI_INIT = "cli_init"
    CLI_GENERATE = "cli_generate"
    CLI_ENRICH = "cli_enrich"


class LogCounterKey(Enum):
    """Set of Counter keys for logging"""

    ASK_DAPI_SERVER_PAYLOAD_ITEMS = "ask_dapi_server_payload_items"
    VALIDATOR_ERRORS = "validator_errors"
    VALIDATOR_ITEMS = "validator_items"


class Timer:
    """A context manager to measure the time taken for a block of code and publish to sentry."""

    def __init__(self, dist_key: LogDistKey, tags=None) -> None:
        """Initialize the timer"""
        self.dist_key = dist_key
        self.tags = tags
        self.start = None

    def __enter__(self):
        """Start the timer"""
        self.start = time.time()
        return self

    def set_tags(self, tags):
        """Set tags for the timer"""
        self.tags = always_merger.merge(self.tags, tags)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End the timer and log the distribution metric to sentry."""
        _end = time.time()
        _elapsed = _end - self.start
        try:
            sentry_sdk.metrics.distribution(
                key=f"opendapi.{self.dist_key}",
                value=_elapsed * 1000,
                unit="milliseconds",
                tags=self.tags,
            )
        except Exception:  # pylint: disable=broad-except
            # Fail silently
            pass  # nosec B110
        return False


def increment_counter(key: LogCounterKey, value: int = 1, tags: dict = None):
    """Increment a counter metric in sentry."""
    try:
        sentry_sdk.metrics.incr(
            key=f"opendapi.{key}",
            value=value,
            tags=tags,
        )
    except Exception:  # pylint: disable=broad-except
        # Fail silently
        pass  # nosec B110


def sentry_init(dapi_server_host: str = None, dapi_server_api_key: str = None):
    """Initialize sentry, but silently fail in case of errors"""
    # Silently return if we don't have the required information
    if not dapi_server_host or not dapi_server_api_key:
        return

    try:
        response = requests.get(
            urljoin(dapi_server_host, "/v1/config/client/opendapi"),
            headers={
                "Content-Type": "application/json",
                DAPI_API_KEY_HEADER: dapi_server_api_key,
            },
            timeout=60,
        )

        # We will silently ignore any errors
        response.raise_for_status()

        # Try and initialize sentry so we can capture all the errors
        config = response.json()
        sentry_config = config.get("sentry", {})
        if sentry_config:
            sentry_config["release"] = version("opendapi")
            sentry_config["event_scrubber"] = sentry_sdk.scrubber.EventScrubber(
                denylist=WOVEN_DENY_LIST
            )
            sentry_config["_experiments"] = {
                # Turns on the metrics module
                "enable_metrics": True,
                # Enables sending of code locations for metrics
                "metric_code_locations": True,
            }
            sentry_sdk.init(**config["sentry"])

        # Set sentry tags
        sentry_tags = config.get("sentry_tags", {})
        if sentry_config and sentry_tags:
            for tag, value in sentry_tags.items():
                sentry_sdk.set_tag(tag, value)

    except Exception:  # pylint: disable=broad-except
        pass  # nosec B110
