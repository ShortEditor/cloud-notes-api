# Task 2: Core Concepts and Skills

Small demonstration of core cloud-service concepts: REST CRUD, configuration from environment variables, logging, and tests. See [docs/concepts.md](docs/concepts.md) for the notes on each concept.

## Run
```
pip install -r requirements.txt -r requirements-dev.txt
PORT=8080 LOG_LEVEL=DEBUG python -m app.main
python -m pytest -q
```

## Endpoints
`GET /health`, `GET/POST /notes`, `GET/PUT/DELETE /notes/<id>`

## Environment variables
| Name | Default | Meaning |
|---|---|---|
| PORT | 8080 | listen port |
| LOG_LEVEL | INFO | logging level |
| MAX_NOTES | 100 | maximum stored notes |

Data is kept in memory only; Task 3 adds persistence.
