"""Simple performance check: bulk inserts and a paged query must stay fast."""
import time

from app import db


def test_bulk_insert_and_query_speed(conn):
    start = time.perf_counter()
    for i in range(500):
        db.create(conn, f"note {i}", "body " * 20)
    insert_s = time.perf_counter() - start
    start = time.perf_counter()
    items, total = db.list_notes(conn, "note 49", 20, 0)
    query_s = time.perf_counter() - start
    assert total >= 1 and len(items) <= 20
    assert insert_s < 5.0
    assert query_s < 0.5
