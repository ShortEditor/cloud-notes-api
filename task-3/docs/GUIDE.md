# Technical guide: Notes API (Task 3)

## Requirements
- Create, read, update and delete notes.
- Data must survive restarts.
- Reject bad input with clear errors; never crash on it.
- Search and paginate the list.
- Be easy to test and to run in a container.

## Architecture
```
client -> Flask routes (app/main.py) -> validation (app/validation.py)
                                      -> data layer (app/db.py) -> SQLite file
```
- `main.py`: routes and error handlers. `create_app(db_path)` is an application factory so each test gets its own database file.
- `validation.py`: pure functions that check payloads and paging parameters. Easy to unit test and reuse.
- `db.py`: all SQL lives here, using parameterised queries only.

## Data model
Table `notes`: `id` (integer primary key), `title` (required), `body`, `created_at`, `updated_at` (UTC ISO timestamps).

## Design decisions
1. SQLite instead of a server database: no extra service to run, standard library only, enough for a single-instance demo. Limitation: one writer, so a multi-instance deployment would need PostgreSQL or similar.
2. Application factory plus a per-request connection stored on Flask `g` and closed on teardown, so no connection is shared between requests.
3. Parameterised SQL for every query, including the search `LIKE`, to avoid SQL injection. A test sends `' OR 1=1 --` and checks it matches nothing.
4. Validation separated from routes, with explicit limits (title 100, body 5000, page size 100) to bound request cost.
5. JSON error responses for 400, 404, 405 and unexpected 500 so clients never receive an HTML error page. Unexpected errors are logged with a traceback but return a generic message.

## Testing
`tests/test_api.py` has 20 test cases (pytest, including parametrised cases). It covers the CRUD flow, persistence across app instances, nine invalid payloads, the 100-character title boundary, search, pagination, bad paging parameters, the injection string, JSON errors and the health check. GitHub Actions runs them on every push.

I also started the server locally, created a note with curl, searched for it and called /health; all returned the expected JSON.

## Known limitations and next steps
- No authentication or rate limiting.
- Search uses `LIKE`, which is slow on large tables; SQLite FTS would be a next step.
- Single instance only (SQLite file).
- The Docker image has not been built or run yet.
- Deployment on a free tier is planned for a later task.
