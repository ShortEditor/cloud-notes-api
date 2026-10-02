# Specification: Notes API v1.0 (capstone)

## Topic and goal
A small, secure, containerised REST service for storing notes. I chose it because it let me apply every topic from this internship (setup, core concepts, a real implementation, testing, deployment) in one project that I can keep extending.

## Features
1. Create, read, update and delete notes (title up to 100 chars, body up to 5000)
2. Search by text, paginated results
3. Persistent storage in SQLite
4. Optional API key for write requests (`X-API-Key`, set with the `API_KEY` variable)
5. Rate limiting per client (`RATE_LIMIT_PER_MIN`, default 120)
6. Health and version endpoints, security headers, JSON errors
7. Docker image, compose file and CI pipeline

## Technical requirements
Python 3.12, Flask, gunicorn, SQLite; configuration from environment variables only; tests with at least 90% coverage; lint clean.

## Timeline (as it actually happened)
Task 1 setup, Task 2 concepts, Task 3 implementation, Task 4 testing, Task 5 deployment pipeline, Task 6 security additions and documentation, all in the task folders of this repository.

## Out of scope
User accounts, a web front end, multi-instance deployment, a hosted public URL.
