# Task 6: Final Project and Assessment - Notes API v1.0

Capstone that combines the earlier tasks into one service: REST CRUD with SQLite, validation, search and paging, optional API key for writes, per-client rate limiting, security headers, health/version endpoints, Docker, CI and documentation.

- [docs/SPEC.md](docs/SPEC.md) - topic, features, requirements, timeline
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - run, configure, use, extend, limits
- [docs/TEST_REPORT.md](docs/TEST_REPORT.md) - test results and self-assessment
- [docs/PRESENTATION.md](docs/PRESENTATION.md) - presentation outline

```
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest        # 81 tests, coverage gate 90%
ruff check .
```
