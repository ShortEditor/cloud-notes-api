# Task 4: Testing and Quality Assurance

The Task 3 Notes API with a full test suite and quality checks added. The application code is the same as Task 3; the work in this folder is the testing.

## Run
```
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest        # runs tests with coverage, fails below 90%
ruff check .            # lint
```

## What is covered
| Type | File | What it checks |
|---|---|---|
| Unit | tests/test_unit_validation.py | validation and paging functions in isolation, boundary values |
| Unit | tests/test_unit_db.py | data layer against a temporary SQLite file |
| Integration | tests/test_integration_api.py | HTTP layer, validation and database together, persistence across app instances |
| Edge cases / errors | tests/test_edge_cases.py | invalid payloads, non-JSON body, unicode, bad paging, SQL injection string, JSON error pages, forced 500 error |
| Performance | tests/test_performance.py | 500 inserts and a search query must stay within time limits |

Results and findings are in [docs/TEST_REPORT.md](docs/TEST_REPORT.md).
