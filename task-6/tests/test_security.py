import pytest

from app.main import create_app
from app.security import RateLimiter, key_ok


def make(tmp_path, monkeypatch, **env):
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return create_app(str(tmp_path / "s.db")).test_client()


def test_no_key_configured_allows_writes(tmp_path, monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    c = make(tmp_path, monkeypatch)
    assert c.post("/notes", json={"title": "a"}).status_code == 201


def test_key_required_for_writes_only(tmp_path, monkeypatch):
    c = make(tmp_path, monkeypatch, API_KEY="s3cret")
    assert c.post("/notes", json={"title": "a"}).status_code == 401
    assert c.post("/notes", json={"title": "a"}, headers={"X-API-Key": "bad"}).status_code == 401
    ok = c.post("/notes", json={"title": "a"}, headers={"X-API-Key": "s3cret"})
    assert ok.status_code == 201
    assert c.get("/notes").status_code == 200
    assert c.delete("/notes/1").status_code == 401
    assert c.delete("/notes/1", headers={"X-API-Key": "s3cret"}).status_code == 204


def test_rate_limit(tmp_path, monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    c = make(tmp_path, monkeypatch, RATE_LIMIT_PER_MIN="3")
    codes = [c.get("/notes").status_code for _ in range(5)]
    assert codes == [200, 200, 200, 429, 429]
    assert c.get("/health").status_code == 200


def test_limiter_window():
    t = [0.0]
    rl = RateLimiter(2, window=10, clock=lambda: t[0])
    assert rl.allow("a") and rl.allow("a") and not rl.allow("a")
    assert rl.allow("b")
    t[0] = 11
    assert rl.allow("a")


@pytest.mark.parametrize("expected,supplied,ok", [(None, None, True), ("", "x", True),
                                                 ("k", None, False), ("k", "k", True), ("k", "K", False)])
def test_key_ok(expected, supplied, ok):
    assert key_ok(expected, supplied) is ok
