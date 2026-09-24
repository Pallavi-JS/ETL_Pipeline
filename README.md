# ETL Pipeline with Unit Tests
**DataGrokr PLP — Week 3 Mini Project (Python, Advanced)**

Fetches user data from a public REST API, transforms it with pandas,
and loads the result into a CSV file — with a full pytest unit test suite.

## Project Structure

```
etl_pipeline/
├── main.py                  # Entry point — run this
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── extract.py           # API call + generator (stream_records)
│   ├── transform.py         # pandas cleaning/reshaping
│   ├── load.py               # write to CSV
│   └── pipeline.py           # orchestrates extract -> transform -> load
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # shared pytest fixtures
│   ├── test_extract.py       # mocks requests.get
│   ├── test_transform.py     # includes pytest.mark.parametrize
│   ├── test_load.py          # uses tmp_path fixture
│   └── test_pipeline.py      # end-to-end integration test
└── output/
    └── users.csv             # created after running main.py
```

## Setup (VS Code)

1. Create the folder structure above (or unzip the provided files) and open
   it in VS Code as your project folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the pipeline

```bash
python main.py
```

This fetches data from `https://jsonplaceholder.typicode.com/users`,
cleans it, and writes `output/users.csv`.

## Run the tests

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

## What each part demonstrates (matches Week 3 syllabus)

| Topic                          | Where |
|---------------------------------|-------|
| Generators / `yield` / lazy eval | `src/extract.py` → `stream_records()` |
| REST API + `requests`            | `src/extract.py` → `fetch_users()` |
| JSON handling                    | `src/transform.py` → `pd.json_normalize` |
| pandas transform                 | `src/transform.py` |
| Full ETL: API → pandas → file    | `src/pipeline.py` → `run_etl()` |
| pytest fixtures                  | `tests/conftest.py`, `test_load.py` |
| pytest parametrize               | `tests/test_transform.py` |
| Mocking external calls           | `tests/test_extract.py`, `tests/test_pipeline.py` |
| Exception handling               | Custom exceptions in every `src/` module |

## Notes

- The tests never hit the real network — `requests.get` is mocked, so the
  suite is fast and works offline.
- `output/users.csv` is generated when you actually run `main.py`, not
  during testing.
