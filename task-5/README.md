# Task 5: Deployment and Production

The Notes API prepared for production: hardened container, automated build and smoke-test pipeline, and a published container image. Runbook: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## What was added to the Task 4 code
- Security headers on every response (`nosniff`, `X-Frame-Options: DENY`, `Cache-Control: no-store`)
- `/version` endpoint (reads `APP_VERSION`) to identify what is running
- Production Dockerfile: non-root user, health check, gunicorn with 2 workers, access log to stdout, data volume
- `docker-compose.yml` for a repeatable local run
- `render.yaml` blueprint for a free Render web service (prepared, not deployed)
- GitHub Actions pipeline `.github/workflows/deploy-task5.yml` at the repo root

## Run locally
```
docker compose up --build        # http://localhost:8080/health
```
or without Docker:
```
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
```
