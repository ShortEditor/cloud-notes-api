# Task 3: Practical Implementation Project

Notes API: a Flask service that stores notes in SQLite, with input validation, search, pagination, JSON error handling, tests and a Dockerfile. The architecture and decisions are in [docs/GUIDE.md](docs/GUIDE.md).

## Run
```
pip install -r requirements.txt -r requirements-dev.txt
DB_PATH=notes.db PORT=8080 python -m app.main
python -m pytest -q        # 20 tests
```

## API
| Method | Path | Notes |
|---|---|---|
| GET | /health | checks the database connection |
| GET | /notes?q=&limit=&offset= | search title/body, paginate (limit 1-100, default 20) |
| POST | /notes | `{"title": "...", "body": "..."}` title required, max 100 chars; body max 5000 |
| GET | /notes/<id> | 404 if missing |
| PUT | /notes/<id> | same payload as POST |
| DELETE | /notes/<id> | 204 on success |

Example:
```
curl -X POST localhost:8080/notes -H 'content-type: application/json' -d '{"title":"Demo","body":"works"}'
```

## Environment variables
`DB_PATH` (default `notes.db`), `PORT` (default 8080), `LOG_LEVEL` (default INFO).

## Docker
```
docker build -t cloud-notes-api-task3 .
docker run -p 8080:8080 -v notes-data:/data cloud-notes-api-task3
```
The Dockerfile has not been built in my environment yet.
