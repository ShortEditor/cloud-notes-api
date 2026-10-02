"""Task 2 demo: REST CRUD, environment config and logging in a small Flask app."""
import logging

from flask import Flask, jsonify, request

from app import config

cfg = config.load()
logging.basicConfig(level=cfg["log_level"], format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("notes")

app = Flask(__name__)
NOTES = {}
_next_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/notes")
def list_notes():
    return jsonify(list(NOTES.values()))


@app.post("/notes")
def create_note():
    global _next_id
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="text is required"), 400
    if len(NOTES) >= cfg["max_notes"]:
        return jsonify(error="note limit reached"), 409
    note = {"id": _next_id, "text": text.strip()}
    NOTES[_next_id] = note
    _next_id += 1
    log.info("created note %s", note["id"])
    return jsonify(note), 201


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = NOTES.get(note_id)
    if note is None:
        return jsonify(error="not found"), 404
    return jsonify(note)


@app.put("/notes/<int:note_id>")
def update_note(note_id):
    if note_id not in NOTES:
        return jsonify(error="not found"), 404
    text = (request.get_json(silent=True) or {}).get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="text is required"), 400
    NOTES[note_id]["text"] = text.strip()
    log.info("updated note %s", note_id)
    return jsonify(NOTES[note_id])


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    if NOTES.pop(note_id, None) is None:
        return jsonify(error="not found"), 404
    log.info("deleted note %s", note_id)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=cfg["port"])
