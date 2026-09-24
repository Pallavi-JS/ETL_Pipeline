
from unittest.mock import Mock, patch

import pandas as pd

from src.pipeline import run_etl


class TestRunEtl:
    @patch("src.extract.requests.get")
    def test_full_pipeline_produces_csv(self, mock_get, sample_raw_records, tmp_path):
        mock_response = Mock()
        mock_response.json.return_value = sample_raw_records
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        output_path = tmp_path / "users.csv"
        result_path = run_etl(api_url="https://fake-api.test/users", output_path=output_path)

        assert result_path.exists()

        df = pd.read_csv(result_path)
        # duplicates + missing-email rows should have been cleaned in transform
        assert len(df) == 2
        assert set(df.columns) == {"id", "name", "username", "email", "city", "company_name"}
