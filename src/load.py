"""
load.py
-------
Load layer of the ETL pipeline.

Writes the cleaned DataFrame to a CSV file on disk.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class LoadError(Exception):
    """Raised when the DataFrame cannot be written to disk."""


def save_to_csv(df: pd.DataFrame, output_path: str | Path) -> Path:
    """
    Save a DataFrame to CSV, creating parent directories if needed.

    Parameters
    ----------
    df : pd.DataFrame
        Data to write.
    output_path : str | Path
        Destination file path.

    Returns
    -------
    Path
        The path the file was written to.

    Raises
    ------
    LoadError
        If df is empty or the write fails.
    """
    if df is None or df.empty:
        raise LoadError("Refusing to write an empty DataFrame to CSV")

    output_path = Path(output_path)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
    except OSError as exc:
        raise LoadError(f"Failed to write CSV to {output_path}: {exc}") from exc

    logger.info("Wrote %d rows to %s", len(df), output_path)
    return output_path
