from app.main import app


def test_hello():
    r = app.test_client().get("/")
    assert r.status_code == 200
    assert r.get_json()["message"] == "Hello, Cloud!"


def test_health():
    r = app.test_client().get("/health")
    assert r.get_json() == {"status": "ok"}
