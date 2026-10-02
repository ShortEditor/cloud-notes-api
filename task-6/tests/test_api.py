import pytest

from app.main import create_app


@pytest.fixture
def c(tmp_path):
    return create_app(str(tmp_path / "t.db")).test_client()


def test_crud_flow(c):
    r = c.post("/notes", json={"title": " First ", "body": "hello"})
    assert r.status_code == 201
    note = r.get_json()
    assert note["title"] == "First" and note["id"] == 1
    assert c.get("/notes/1").get_json()["body"] == "hello"
    r = c.put("/notes/1", json={"title": "Edited", "body": "x"})
    assert r.get_json()["title"] == "Edited"
    assert c.delete("/notes/1").status_code == 204
    assert c.get("/notes/1").status_code == 404


def test_persistence_across_app_instances(tmp_path):
    path = str(tmp_path / "p.db")
    create_app(path).test_client().post("/notes", json={"title": "keep"})
    items = create_app(path).test_client().get("/notes").get_json()["items"]
    assert [n["title"] for n in items] == ["keep"]


@pytest.mark.parametrize(
    "body",
    [None, [], {}, {"title": ""}, {"title": "  "}, {"title": 3}, {"title": "a", "body": 5},
     {"title": "x" * 101}, {"title": "a", "body": "y" * 5001}],
)
def test_invalid_payloads(c, body):
    assert c.post("/notes", json=body).status_code == 400


def test_title_boundary(c):
    assert c.post("/notes", json={"title": "x" * 100}).status_code == 201


def test_search_and_pagination(c):
    for i in range(5):
        c.post("/notes", json={"title": f"note {i}", "body": "apple" if i % 2 else "pear"})
    r = c.get("/notes?limit=2&offset=1").get_json()
    assert [n["id"] for n in r["items"]] == [2, 3] and r["total"] == 5
    r = c.get("/notes?q=apple").get_json()
    assert r["total"] == 2


@pytest.mark.parametrize("qs", ["limit=0", "limit=101", "limit=abc", "offset=-1"])
def test_bad_paging(c, qs):
    assert c.get(f"/notes?{qs}").status_code == 400


def test_sql_injection_is_inert(c):
    c.post("/notes", json={"title": "a"})
    r = c.get("/notes?q=' OR 1=1 --")
    assert r.get_json()["total"] == 0
    assert c.get("/notes").get_json()["total"] == 1


def test_errors_are_json(c):
    assert c.get("/nope").get_json() == {"error": "not found"}
    assert c.patch("/notes/1").status_code == 405
    assert c.put("/notes/99", json={"title": "x"}).status_code == 404
    assert c.delete("/notes/99").status_code == 404


def test_health(c):
    assert c.get("/health").get_json() == {"status": "ok"}
