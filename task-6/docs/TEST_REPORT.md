# Final test and assessment report

- 81 tests, all passing locally (Python 3.10); CI runs them on Python 3.12.
- Coverage 99% (gate at 90%); the only uncovered line is `app.run` in `__main__`.
- Lint (ruff) clean.
- Security tests: API key required for writes only, wrong key rejected, rate limit returns 429 and excludes health, limiter window resets, key comparison cases.
- Manual check: I started the server with an API key and used curl. A POST without a key returned 401, with the key it created a note, search found it, and the health response carried the `nosniff` header.

## Self-assessment against the internship objectives
- Environment and Git/GitHub: done (Task 1).
- Core concepts: REST, configuration, logging (Task 2).
- Implementation, testing and documentation: done (Tasks 3, 4, 6).
- Deployment: container and pipeline prepared; not running on a live host (Task 5).
- Not done: peer code review or stakeholder presentation; the outline in PRESENTATION.md is prepared for when one is possible.
