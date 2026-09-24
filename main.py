
import logging

from src.pipeline import run_etl

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    path = run_etl()
    print(f"\nETL complete. Data written to: {path.resolve()}")
