from datetime import datetime
from types import SimpleNamespace
import uuid

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.users.models import UserRole


class DummySession:
    def close(self):
        pass


class FakeRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, ex=None):
        self.store[key] = value
        return True

    def delete(self, key):
        self.store.pop(key, None)
        return 1

    def expire(self, key, seconds):
        return key in self.store


@pytest.fixture(autouse=True)
def isolate_external_services(monkeypatch):
    fake_redis = FakeRedis()

    monkeypatch.setattr("src.middleware.logging.LocalSession", lambda: DummySession())
    monkeypatch.setattr("src.middleware.logging.create_api_log", lambda **kwargs: None)
    monkeypatch.setattr("src.users.controllers.redis_client", fake_redis)
    monkeypatch.setattr("src.utils.helper.redis_client", fake_redis)
    monkeypatch.setattr("src.blogs.controllers.redis_client", fake_redis)

    app.dependency_overrides.clear()
    yield fake_redis
    app.dependency_overrides.clear()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def fake_user():
    return SimpleNamespace(
        id=uuid.uuid4(),
        name="Test Author",
        email="author@example.com",
        role=UserRole.AUTHOR,
        created_at=datetime.now(),
    )


@pytest.fixture()
def blog_payload():
    return {
        "title": "Testing FastAPI",
        "introduction": "Intro",
        "content": "Body",
        "conclusion": "Done",
        "slug": "testing-fastapi",
        "meta_description": "A short test blog",
        "keywords": ["fastapi", "tests"],
    }
