"""
test_load.py
------------
Unit tests for the load layer.

Uses pytest's built-in tmp_path fixture so tests write to a throwaway
temp directory instead of touching real project files.
"""

import pandas as pd
import pytest

from src.load import LoadError, save_to_csv


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Leanne Graham", "Ervin Howell"],
            "email": ["Sincere@april.biz", "Shanna@melissa.tv"],
        }
    )


class TestSaveToCsv:
    def test_writes_file_to_disk(self, sample_df, tmp_path):
        output_path = tmp_path / "users.csv"
        result_path = save_to_csv(sample_df, output_path)

        assert result_path == output_path
        assert output_path.exists()

    def test_written_csv_matches_dataframe(self, sample_df, tmp_path):
        output_path = tmp_path / "users.csv"
        save_to_csv(sample_df, output_path)

        reloaded = pd.read_csv(output_path)
        pd.testing.assert_frame_equal(reloaded, sample_df)

    def test_creates_missing_parent_directories(self, sample_df, tmp_path):
        nested_path = tmp_path / "nested" / "dir" / "users.csv"
        save_to_csv(sample_df, nested_path)
        assert nested_path.exists()

    def test_empty_dataframe_raises(self, tmp_path):
        empty_df = pd.DataFrame()
        with pytest.raises(LoadError):
            save_to_csv(empty_df, tmp_path / "users.csv")

    def test_none_dataframe_raises(self, tmp_path):
        with pytest.raises(LoadError):
            save_to_csv(None, tmp_path / "users.csv")
