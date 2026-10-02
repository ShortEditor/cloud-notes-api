"""Integration tests: HTTP layer + validation + database together."""

from app.main import create_app


def test_crud_flow(client):
    r = client.post("/notes", json={"title": " First ", "body": "hello"})
    assert r.status_code == 201 and r.get_json()["title"] == "First"
    assert client.get("/notes/1").get_json()["body"] == "hello"
    assert client.put("/notes/1", json={"title": "Edited"}).get_json()["title"] == "Edited"
    assert client.delete("/notes/1").status_code == 204
    assert client.get("/notes/1").status_code == 404


def test_persistence_across_app_instances(tmp_path):
    path = str(tmp_path / "p.db")
    create_app(path).test_client().post("/notes", json={"title": "keep"})
    items = create_app(path).test_client().get("/notes").get_json()["items"]
    assert [n["title"] for n in items] == ["keep"]


def test_search_and_paging(client):
    for i in range(5):
        client.post("/notes", json={"title": f"n{i}", "body": "apple" if i % 2 else "pear"})
    r = client.get("/notes?limit=2&offset=1").get_json()
    assert [n["id"] for n in r["items"]] == [2, 3] and r["total"] == 5
    assert client.get("/notes?q=apple").get_json()["total"] == 2
