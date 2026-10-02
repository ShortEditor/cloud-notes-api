"""SQLite data layer for notes. Uses parameterised queries only."""
import sqlite3
from datetime import datetime, timezone


def connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "title TEXT NOT NULL,"
        "body TEXT NOT NULL DEFAULT '',"
        "created_at TEXT NOT NULL,"
        "updated_at TEXT NOT NULL)"
    )
    return conn


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def row_to_dict(row):
    return {k: row[k] for k in row.keys()}


def create(conn, title, body):
    now = _now()
    cur = conn.execute(
        "INSERT INTO notes (title, body, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (title, body, now, now),
    )
    conn.commit()
    return get(conn, cur.lastrowid)


def get(conn, note_id):
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return row_to_dict(row) if row else None


def list_notes(conn, q=None, limit=20, offset=0):
    if q:
        rows = conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY id LIMIT ? OFFSET ?",
            (f"%{q}%", f"%{q}%", limit, offset),
        ).fetchall()
        total = conn.execute(
            "SELECT COUNT(*) FROM notes WHERE title LIKE ? OR body LIKE ?", (f"%{q}%", f"%{q}%")
        ).fetchone()[0]
    else:
        rows = conn.execute(
            "SELECT * FROM notes ORDER BY id LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    return [row_to_dict(r) for r in rows], total


def update(conn, note_id, title, body):
    cur = conn.execute(
        "UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?",
        (title, body, _now(), note_id),
    )
    conn.commit()
    return get(conn, note_id) if cur.rowcount else None


def delete(conn, note_id):
    cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    return cur.rowcount > 0
