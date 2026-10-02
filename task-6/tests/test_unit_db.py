"""Unit tests: data layer against a temporary SQLite file."""
from app import db


def test_create_get(conn):
    n = db.create(conn, "t", "b")
    assert n["id"] == 1 and n["title"] == "t" and n["created_at"] == n["updated_at"]
    assert db.get(conn, 1) == n
    assert db.get(conn, 2) is None


def test_update_and_delete(conn):
    db.create(conn, "t", "b")
    assert db.update(conn, 1, "new", "body")["title"] == "new"
    assert db.update(conn, 9, "x", "y") is None
    assert db.delete(conn, 1) is True
    assert db.delete(conn, 1) is False


def test_list_search_paging(conn):
    for i in range(10):
        db.create(conn, f"t{i}", "red" if i < 3 else "blue")
    items, total = db.list_notes(conn, None, 4, 8)
    assert total == 10 and [n["id"] for n in items] == [9, 10]
    items, total = db.list_notes(conn, "red", 20, 0)
    assert total == 3


def test_like_wildcards_are_parameters(conn):
    db.create(conn, "plain", "")
    assert db.list_notes(conn, "'; DROP TABLE notes; --", 20, 0)[1] == 0
    assert db.list_notes(conn, None, 20, 0)[1] == 1
