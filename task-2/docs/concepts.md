# Core concepts practised in Task 2

Each concept below is demonstrated by a small piece of code in this folder.

## 1. REST resources and HTTP status codes
Notes are a resource at `/notes`. POST creates (201), GET reads (200), PUT updates (200), DELETE removes (204). Bad input returns 400, a missing note 404, and exceeding the limit 409. Using the right status code lets clients and load balancers react without parsing text.

## 2. Configuration through environment variables
`app/config.py` reads `PORT`, `LOG_LEVEL` and `MAX_NOTES`. The same container image can run in different environments with different settings and no code change. Secrets would be passed the same way, never committed.

## 3. Logging
`app/main.py` logs each create, update and delete with a timestamp and level. In a container, writing logs to stdout lets the platform collect them.

## 4. Statelessness (and its limit)
Notes live in process memory. That is simple, but data is lost on restart and two instances would not share it. This is the known pitfall of this task's design, and Task 3 moves the data into SQLite.

## 5. Automated tests
`tests/test_notes.py` covers the happy path, update/delete, invalid input (parametrised), the configurable limit and missing ids.

## Common pitfalls noted
- Trusting request JSON without validation.
- Hard-coding ports and settings.
- Keeping state in memory in a service meant to scale out.
