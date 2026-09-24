

from __future__ import annotations

import logging
from typing import Iterator

import requests

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://jsonplaceholder.typicode.com/users"
REQUEST_TIMEOUT = 10  # seconds


class ExtractionError(Exception):
    """Raised when the API call fails or returns unusable data."""


def fetch_users(api_url: str = DEFAULT_API_URL) -> list[dict]:
    """
    Fetch the raw list of user records from the REST API.

    Parameters
    ----------
    api_url : str
        The endpoint to call.

    Returns
    -------
    list[dict]
        Raw JSON records exactly as returned by the API.

    Raises
    ------
    ExtractionError
        If the request fails, times out, or the response is not valid JSON.
    """
    try:
        response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("Failed to fetch data from %s: %s", api_url, exc)
        raise ExtractionError(f"Could not fetch data from {api_url}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ExtractionError("API response was not valid JSON") from exc

    if not isinstance(data, list):
        raise ExtractionError("Expected a JSON list of records from the API")

    logger.info("Fetched %d records from %s", len(data), api_url)
    return data


def stream_records(records: list[dict]) -> Iterator[dict]:
    """
    Lazily yield one record at a time.

    A generator is used here (per the Week 3 syllabus: yield / lazy
    evaluation) so large payloads could be processed without loading
    everything into memory at once downstream.
    """
    for record in records:
        yield record
