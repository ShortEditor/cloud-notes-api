"""Edge cases and error handling."""
import pytest


@pytest.mark.parametrize(
    "body",
    [None, [], {}, {"title": ""}, {"title": "  "}, {"title": 3}, {"title": "a", "body": 5},
     {"title": "x" * 101}, {"title": "a", "body": "y" * 5001}],
)
def test_invalid_payloads(client, body):
    assert client.post("/notes", json=body).status_code == 400


def test_non_json_body(client):
    r = client.post("/notes", data="not json", content_type="text/plain")
    assert r.status_code == 400


def test_unicode_roundtrip(client):
    r = client.post("/notes", json={"title": "నమస్తే", "body": "héllo 😀"})
    assert client.get(f"/notes/{r.get_json()['id']}").get_json()["title"] == "నమస్తే"


@pytest.mark.parametrize("qs", ["limit=0", "limit=101", "limit=abc", "offset=-1"])
def test_bad_paging(client, qs):
    assert client.get(f"/notes?{qs}").status_code == 400


def test_injection_is_inert(client):
    client.post("/notes", json={"title": "a"})
    assert client.get("/notes?q=' OR 1=1 --").get_json()["total"] == 0


def test_json_errors(client):
    assert client.get("/nope").get_json() == {"error": "not found"}
    assert client.patch("/notes/1").status_code == 405
    assert client.put("/notes/99", json={"title": "x"}).status_code == 404
    assert client.delete("/notes/99").status_code == 404
    assert client.get("/notes/abc").status_code == 404


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_unexpected_error_returns_generic_json(tmp_path, monkeypatch):
    from app import db
    from app.main import create_app

    def boom(*args, **kwargs):
        raise RuntimeError("secret internal detail")

    monkeypatch.setattr(db, "list_notes", boom)
    app = create_app(str(tmp_path / "e.db"))
    app.config["PROPAGATE_EXCEPTIONS"] = False
    r = app.test_client().get("/notes")
    assert r.status_code == 500
    assert r.get_json() == {"error": "internal server error"}
    assert "secret" not in r.get_data(as_text=True)


def test_put_invalid_payload(client):
    client.post("/notes", json={"title": "a"})
    assert client.put("/notes/1", json={"title": ""}).status_code == 400
