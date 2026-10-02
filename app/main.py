"""Hello World API for the cloud-notes-api project (Task 1: setup milestone)."""
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def hello():
    return jsonify(message="Hello, Cloud!", service="cloud-notes-api")


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
