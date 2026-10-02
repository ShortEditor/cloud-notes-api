import pytest

from app import db
from app.main import create_app


@pytest.fixture
def conn(tmp_path):
    c = db.connect(str(tmp_path / "unit.db"))
    yield c
    c.close()


@pytest.fixture
def client(tmp_path):
    return create_app(str(tmp_path / "api.db")).test_client()
