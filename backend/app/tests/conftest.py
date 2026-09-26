import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="wp-test-")

import pytest
from fastapi.testclient import TestClient

from app import seed
from app.config import DB_PATH
from app.main import app


@pytest.fixture(autouse=True)
def fresh_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    seed.init_db()
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
