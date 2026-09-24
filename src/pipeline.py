

from __future__ import annotations

import logging
from pathlib import Path

from src.extract import DEFAULT_API_URL, fetch_users
from src.load import save_to_csv
from src.transform import transform_users

logger = logging.getLogger(__name__)


def run_etl(api_url: str = DEFAULT_API_URL, output_path: str | Path = "output/users.csv") -> Path:
    """
    Run the full ETL pipeline end to end.

    Parameters
    ----------
    api_url : str
        REST API endpoint to extract from.
    output_path : str | Path
        Where to write the final CSV.

    Returns
    -------
    Path
        Path to the written CSV file.
    """
    logger.info("Starting ETL run: %s -> %s", api_url, output_path)

    raw_records = fetch_users(api_url)
    clean_df = transform_users(raw_records)
    written_path = save_to_csv(clean_df, output_path)

    logger.info("ETL run complete.")
    return written_path


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    run_etl()
