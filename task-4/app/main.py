"""Task 3: Notes API with SQLite persistence, validation and error handling."""
import logging
import os

from flask import Flask, g, jsonify, request

from app import db
from app.validation import parse_page, validate_note

log = logging.getLogger("notes")


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.environ.get("DB_PATH", "notes.db")
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    def conn():
        if "db" not in g:
            g.db = db.connect(app.config["DB_PATH"])
        return g.db

    @app.teardown_appcontext
    def close(_exc):
        c = g.pop("db", None)
        if c is not None:
            c.close()

    @app.get("/health")
    def health():
        conn().execute("SELECT 1")
        return jsonify(status="ok")

    @app.get("/notes")
    def list_notes():
        limit, offset, err = parse_page(request.args)
        if err:
            return jsonify(error=err), 400
        items, total = db.list_notes(conn(), request.args.get("q"), limit, offset)
        return jsonify(items=items, total=total, limit=limit, offset=offset)

    @app.post("/notes")
    def create_note():
        clean, err = validate_note(request.get_json(silent=True))
        if err:
            return jsonify(error=err), 400
        note = db.create(conn(), clean["title"], clean["body"])
        log.info("created note %s", note["id"])
        return jsonify(note), 201

    @app.get("/notes/<int:note_id>")
    def get_note(note_id):
        note = db.get(conn(), note_id)
        if note is None:
            return jsonify(error="not found"), 404
        return jsonify(note)

    @app.put("/notes/<int:note_id>")
    def update_note(note_id):
        clean, err = validate_note(request.get_json(silent=True))
        if err:
            return jsonify(error=err), 400
        note = db.update(conn(), note_id, clean["title"], clean["body"])
        if note is None:
            return jsonify(error="not found"), 404
        return jsonify(note)

    @app.delete("/notes/<int:note_id>")
    def delete_note(note_id):
        if not db.delete(conn(), note_id):
            return jsonify(error="not found"), 404
        return "", 204

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify(error="not found"), 404

    @app.errorhandler(405)
    def bad_method(_e):
        return jsonify(error="method not allowed"), 405

    @app.errorhandler(Exception)
    def unexpected(e):
        log.exception("unhandled error: %s", e)
        return jsonify(error="internal server error"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
