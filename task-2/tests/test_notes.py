import pytest

from app import main


@pytest.fixture(autouse=True)
def reset():
    main.NOTES.clear()
    main._next_id = 1
    yield


def client():
    return main.app.test_client()


def test_create_and_get():
    r = client().post("/notes", json={"text": "  hello "})
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "text": "hello"}
    assert client().get("/notes/1").get_json()["text"] == "hello"


def test_list_update_delete():
    c = client()
    c.post("/notes", json={"text": "a"})
    c.post("/notes", json={"text": "b"})
    assert len(c.get("/notes").get_json()) == 2
    assert c.put("/notes/1", json={"text": "z"}).get_json()["text"] == "z"
    assert c.delete("/notes/2").status_code == 204
    assert c.get("/notes/2").status_code == 404


@pytest.mark.parametrize("body", [{}, {"text": ""}, {"text": "   "}, {"text": 5}])
def test_bad_input(body):
    assert client().post("/notes", json=body).status_code == 400


def test_limit(monkeypatch):
    monkeypatch.setitem(main.cfg, "max_notes", 1)
    c = client()
    assert c.post("/notes", json={"text": "a"}).status_code == 201
    assert c.post("/notes", json={"text": "b"}).status_code == 409


def test_missing():
    assert client().put("/notes/9", json={"text": "x"}).status_code == 404
    assert client().delete("/notes/9").status_code == 404
