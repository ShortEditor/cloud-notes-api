def test_security_headers(tmp_path):
    from app.main import create_app

    r = create_app(str(tmp_path / "s.db")).test_client().get("/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["Cache-Control"] == "no-store"


def test_version_from_env(tmp_path, monkeypatch):
    from app.main import create_app

    monkeypatch.setenv("APP_VERSION", "1.2.3")
    r = create_app(str(tmp_path / "v.db")).test_client().get("/version")
    assert r.get_json() == {"version": "1.2.3"}
