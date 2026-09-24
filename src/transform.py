

from __future__ import annotations

import logging
from typing import Iterable

import pandas as pd

logger = logging.getLogger(__name__)

# Columns we want in the final, cleaned output
OUTPUT_COLUMNS = ["id", "name", "username", "email", "city", "company_name"]


class TransformationError(Exception):
    """Raised when incoming records cannot be transformed."""


def transform_users(records: Iterable[dict]) -> pd.DataFrame:
    """
    Convert raw user records into a cleaned DataFrame.

    Steps:
      1. Normalize nested JSON (address.city, company.name) into flat columns.
      2. Select and rename only the columns we care about.
      3. Drop rows missing an email (treated as invalid records).
      4. Deduplicate on 'id'.

    Parameters
    ----------
    records : Iterable[dict]
        Raw records, e.g. from extract.fetch_users() or extract.stream_records().

    Returns
    -------
    pd.DataFrame
        Cleaned, flat DataFrame with columns OUTPUT_COLUMNS.

    Raises
    ------
    TransformationError
        If records is empty or missing required base fields.
    """
    records = list(records)
    if not records:
        raise TransformationError("No records to transform")

    try:
        df = pd.json_normalize(records)
    except Exception as exc:  # pragma: no cover - defensive
        raise TransformationError(f"Could not normalize records: {exc}") from exc

    # Flatten nested fields safely (some records may lack them)
    df["city"] = df.get("address.city", pd.Series(dtype="object"))
    df["company_name"] = df.get("company.name", pd.Series(dtype="object"))

    missing = [col for col in ("id", "name", "username", "email") if col not in df.columns]
    if missing:
        raise TransformationError(f"Missing required fields in source data: {missing}")

    df = df[OUTPUT_COLUMNS]

    before = len(df)
    df = df.dropna(subset=["email"])
    df = df.drop_duplicates(subset=["id"])
    after = len(df)

    logger.info("Transformed %d raw records -> %d clean rows", before, after)
    return df.reset_index(drop=True)
