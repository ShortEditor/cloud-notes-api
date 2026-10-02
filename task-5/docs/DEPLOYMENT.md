# Deployment runbook (Task 5)

## 1. Preparing the application
- Dependencies are pinned in `requirements.txt`.
- All settings come from environment variables (`PORT`, `DB_PATH`, `LOG_LEVEL`, `APP_VERSION`); no secrets are stored in the repository.
- Hardening: container runs as a non-root user (uid 10001), responses carry security headers, errors return generic JSON without internal details, SQL is parameterised.
- Tests (52, 99% coverage) run in CI before anything is built.

## 2. Production environment
- Runtime: the Docker image, started by gunicorn with 2 workers.
- Storage: SQLite file on the `/data` volume, so data survives container restarts. Limitation: one instance only, and no automated backup. Backup would be copying the `notes.db` file from the volume.
- Hosting: the image is published to GitHub Container Registry. A Render free-tier blueprint (`render.yaml`) is included, but I have not deployed it, because it needs the account owner to connect Render to GitHub.

## 3. Deployment pipeline
`.github/workflows/deploy-task5.yml` runs on every push that changes `task-5/`:
1. **Staging smoke test**: builds the image on a clean runner, starts the container, then checks `/health`, creates a note, searches for it and checks a security header. The container logs are always printed.
2. **Publish**: only if staging passes, the image is pushed to `ghcr.io/shorteditor/cloud-notes-api` tagged `latest` and with the commit SHA.

In this project, "staging" is the container started on the CI runner. It is a clean replica of the production image, but it is not a separate long-running server.

## 4. Monitoring and logs
- `/health` checks the database connection and is used by the Docker `HEALTHCHECK`.
- `/version` shows the running version.
- gunicorn writes access logs and the app writes application logs to stdout: `docker logs <container>`.

## 5. Troubleshooting and rollback
- Container unhealthy: check `docker logs`, then `/health`. A failing health check usually means the `/data` volume is not writable.
- Roll back: run the previous image tag, e.g. `docker run ... ghcr.io/shorteditor/cloud-notes-api:<previous-sha>`. Every build has an immutable SHA tag.
- Data is not touched by a rollback since it lives on the volume.

## 6. What is not done
- No hosted public URL: the app is not running on a live server.
- The pipeline was written and pushed; whether its first run passes is checked after pushing (see the repository Actions tab).
- No metrics dashboard or alerting; only logs and health checks.
