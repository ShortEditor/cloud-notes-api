# cloud-notes-api

A small Python (Flask) web API used as a learning project for a Cloud Computing internship. It will grow across the internship tasks into a containerised, tested and deployed service.

## Task 1: Fundamentals and Setup

Done in this milestone:
- Git repository and GitHub remote set up
- Python 3.12 environment with a virtualenv
- Hello World API (`GET /` and `GET /health`)
- Unit tests with pytest
- Dockerfile for containerised runs
- GitHub Actions workflow that runs the tests on every push

## Project structure
```
app/main.py       Flask app
tests/            pytest tests
Dockerfile        container image
.github/workflows CI
docs/             notes
```

## Setup
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m app.main        # http://localhost:8080/
python -m pytest -q
```

Docker (optional):
```
docker build -t cloud-notes-api .
docker run -p 8080:8080 cloud-notes-api
```

## Roadmap
Core concepts, a notes CRUD feature, more tests, deployment on a free tier, and a final assessment project.
