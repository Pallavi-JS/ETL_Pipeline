

import pandas as pd
import pytest

from src.transform import OUTPUT_COLUMNS, TransformationError, transform_users


class TestTransformUsers:
    def test_returns_dataframe_with_expected_columns(self, sample_raw_records):
        df = transform_users(sample_raw_records)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == OUTPUT_COLUMNS

    def test_drops_duplicate_ids(self, sample_raw_records):
        df = transform_users(sample_raw_records)
        assert df["id"].is_unique

    def test_drops_rows_with_missing_email(self, sample_raw_records):
        df = transform_users(sample_raw_records)
        assert df["email"].isna().sum() == 0
        assert 3 not in df["id"].values  # id=3 had no email

    def test_row_count_after_cleaning(self, sample_raw_records):
        # 4 raw records -> 1 duplicate + 1 missing-email dropped -> 2 remain
        df = transform_users(sample_raw_records)
        assert len(df) == 2

    def test_flattens_nested_city_and_company(self, sample_raw_records):
        df = transform_users(sample_raw_records)
        row = df.iloc[0]
        assert row["city"] == "Gwenborough"
        assert row["company_name"] == "Romaguera-Crona"

    def test_empty_input_raises(self):
        with pytest.raises(TransformationError):
            transform_users([])

    def test_missing_required_field_raises(self):
        bad_records = [{"id": 1, "username": "x"}]  # no name, no email
        with pytest.raises(TransformationError):
            transform_users(bad_records)

    @pytest.mark.parametrize(
        "field_to_check, expected_dtype_kind",
        [
            ("id", "i"),       # integer
            ("name", "O"),     # object/string
            ("email", "O"),
        ],
    )
    def test_column_dtypes(self, sample_raw_records, field_to_check, expected_dtype_kind):
        df = transform_users(sample_raw_records)
        assert df[field_to_check].dtype.kind == expected_dtype_kind
