# Test report (Task 4)

Run on Python 3.10 locally; GitHub Actions runs the same suite on Python 3.12.

## Result
- 50 tests, all passing.
- Line coverage 99% (db.py 100%, validation.py 100%, main.py 99%; the only uncovered line is the `app.run` call in `__main__`).
- Lint (ruff): no issues.
- Coverage gate: the suite fails if coverage drops below 90%.

## Test types
1. Unit tests for validation and the data layer.
2. Integration tests through the Flask test client against a real temporary SQLite file.
3. Edge cases and error handling: empty, wrong-typed and oversized input, non-JSON requests, unicode text, bad paging values, SQL-injection style input, unknown routes and methods, and a forced internal error.
4. A simple performance check (500 inserts under 5 seconds, a search under 0.5 seconds). It is a guard against regressions, not a benchmark.

## Debugging and findings
- When the suite was first run, coverage showed the generic 500 error handler and the PUT validation branch were not tested. I added tests for both.
- The forced 500 test confirms the response does not leak the internal exception message.
- Ruff reported an unused import in a test file, which I removed.

## Code review
I reviewed the code myself against a checklist: all SQL is parameterised, all inputs are validated with limits, errors return JSON, and no secrets are in the repository. I did not have a peer review for this task, so none is claimed.

## Known issues
- Search uses LIKE and will be slow on large tables.
- No authentication or rate limiting yet.
- The performance test measures a small local dataset only.
