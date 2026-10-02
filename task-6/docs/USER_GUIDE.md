# User guide

## Start
```
pip install -r requirements.txt -r requirements-dev.txt
API_KEY=mysecret DB_PATH=notes.db python -m app.main
```
or `docker compose up --build`.

## Settings (environment variables)
| Name | Default | Meaning |
|---|---|---|
| PORT | 8080 | listen port |
| DB_PATH | notes.db | SQLite file |
| LOG_LEVEL | INFO | log level |
| API_KEY | not set | if set, POST/PUT/DELETE need header `X-API-Key` |
| RATE_LIMIT_PER_MIN | 120 | requests per client per minute (health/version excluded) |
| APP_VERSION | dev | shown by /version |

## Examples
```
curl -X POST localhost:8080/notes -H 'content-type: application/json' -H 'X-API-Key: mysecret' -d '{"title":"Idea","body":"text"}'
curl 'localhost:8080/notes?q=Idea&limit=10&offset=0'
curl -X PUT localhost:8080/notes/1 -H 'content-type: application/json' -H 'X-API-Key: mysecret' -d '{"title":"New title"}'
curl -X DELETE localhost:8080/notes/1 -H 'X-API-Key: mysecret'
```

## Status codes
200/201/204 success; 400 invalid input; 401 bad or missing API key; 404 not found; 405 wrong method; 429 rate limit; 500 unexpected error.

## Maintain and extend
- Run `python -m pytest` and `ruff check .` before every change.
- Add new routes in `app/main.py`, SQL in `app/db.py`, input rules in `app/validation.py`.
- Back up by copying the SQLite file.

## Known limitations
The rate limiter is in memory and per worker process (two gunicorn workers allow up to double the limit), and it identifies clients by IP address, which behind a proxy would be the proxy. The API key is a single shared key, not user accounts. SQLite means one instance.
