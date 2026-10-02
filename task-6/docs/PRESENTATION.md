# Capstone presentation: Notes API v1.0

(Outline for presenting to a mentor or reviewers.)

1. **Problem and goal**: a minimal, production-minded REST service, built step by step during the internship.
2. **Architecture**: Flask routes -> validation -> SQLite data layer; security module for API key and rate limits.
3. **Journey**: Task 1 environment and Hello World; Task 2 REST, config and logging; Task 3 SQLite and validation; Task 4 50 tests and a coverage gate; Task 5 hardened container and CI smoke test; Task 6 API key, rate limiting and documentation.
4. **Decisions**: SQLite for simplicity, parameterised SQL, validation separated from routes, configuration from the environment, constant-time API key comparison.
5. **Quality**: 81 tests, 99% coverage, lint clean, CI on every push.
6. **Lessons**: test edge cases explicitly, keep layers separate, document limits honestly.
7. **Next steps**: live deployment on a hosting service, PostgreSQL, user accounts, shared rate limiting, metrics.
