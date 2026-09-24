

from unittest.mock import Mock, patch

import pytest
import requests

from src.extract import ExtractionError, fetch_users, stream_records


class TestFetchUsers:
    @patch("src.extract.requests.get")
    def test_fetch_users_success(self, mock_get, sample_raw_records):
        mock_response = Mock()
        mock_response.json.return_value = sample_raw_records
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_users("https://fake-api.test/users")

        assert result == sample_raw_records
        mock_get.assert_called_once_with("https://fake-api.test/users", timeout=10)

    @patch("src.extract.requests.get")
    def test_fetch_users_raises_on_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("boom")

        with pytest.raises(ExtractionError):
            fetch_users("https://fake-api.test/users")

    @patch("src.extract.requests.get")
    def test_fetch_users_raises_on_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        mock_get.return_value = mock_response

        with pytest.raises(ExtractionError):
            fetch_users("https://fake-api.test/users")

    @patch("src.extract.requests.get")
    def test_fetch_users_raises_on_bad_json(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("not json")
        mock_get.return_value = mock_response

        with pytest.raises(ExtractionError):
            fetch_users("https://fake-api.test/users")

    @patch("src.extract.requests.get")
    def test_fetch_users_raises_when_response_not_a_list(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"unexpected": "dict"}
        mock_get.return_value = mock_response

        with pytest.raises(ExtractionError):
            fetch_users("https://fake-api.test/users")


class TestStreamRecords:
    def test_stream_records_is_a_generator(self, sample_raw_records):
        gen = stream_records(sample_raw_records)
        # A generator object, not a list -- confirms lazy evaluation
        assert hasattr(gen, "__next__")

    def test_stream_records_yields_all_records_in_order(self, sample_raw_records):
        result = list(stream_records(sample_raw_records))
        assert result == sample_raw_records

    def test_stream_records_empty_input(self):
        assert list(stream_records([])) == []
