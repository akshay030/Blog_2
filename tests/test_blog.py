import uuid
from datetime import datetime

import pytest
from fastapi import HTTPException

from src.blogs import controllers
from src.blogs.models import BlogModel
from src.blogs.schemas import BlogResponseSchema, UpdateBlogSchema
from src.main import app
from src.users.models import UserRole
from src.utils.helper import is_authenticated


def test_get_all_blogs_returns_controller_data(client, monkeypatch):
    blog_id = uuid.uuid4()
    user_id = uuid.uuid4()
    now = datetime.now()

    expected = [
        {
            "id": str(blog_id),
            "title": "Testing FastAPI",
            "introduction": "Intro",
            "content": "Body",
            "conclusion": "Done",
            "slug": "testing-fastapi",
            "meta_description": "A short test blog",
            "keywords": ["fastapi", "tests"],
            "user_id": str(user_id),
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
    ]

    monkeypatch.setattr("src.blogs.controllers.get_all_blogs", lambda db: expected)

    response = client.get("/blogs/")

    assert response.status_code == 200
    assert response.json() == expected


def test_create_blog_requires_authentication(client, blog_payload):
    response = client.post("/blogs/", json=blog_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_create_blog_with_author_returns_created_blog(
    client,
    monkeypatch,
    fake_user,
    blog_payload,
):
    blog_id = uuid.uuid4()
    now = datetime.now()

    app.dependency_overrides[is_authenticated] = lambda: fake_user

    def fake_create_blog(body, db, user):
        assert body.title == blog_payload["title"]
        assert user.id == fake_user.id
        return BlogResponseSchema(
            id=blog_id,
            user_id=fake_user.id,
            created_at=now,
            updated_at=now,
            **body.model_dump(),
        )

    monkeypatch.setattr("src.blogs.controllers.create_blog", fake_create_blog)

    response = client.post("/blogs/", json=blog_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == str(blog_id)
    assert data["title"] == blog_payload["title"]
    assert data["user_id"] == str(fake_user.id)


def test_update_blog_rejects_non_owner_author(fake_user):
    blog = BlogModel(
        id=uuid.uuid4(),
        title="Old title",
        introduction="Intro",
        content="Body",
        conclusion="Done",
        slug="old-title",
        meta_description="Description",
        keywords=["old"],
        user_id=uuid.uuid4(),
    )
    db = FakeDb(blog)

    with pytest.raises(HTTPException) as exc:
        controllers.update_blog(
            blog.id,
            UpdateBlogSchema(title="New title"),
            db,
            fake_user,
        )

    assert exc.value.status_code == 403
    assert exc.value.detail == "You are not allowed"


def test_update_blog_allows_admin_to_edit_other_users_blog(fake_user):
    fake_user.role = UserRole.ADMIN
    blog = BlogModel(
        id=uuid.uuid4(),
        title="Old title",
        introduction="Intro",
        content="Body",
        conclusion="Done",
        slug="old-title",
        meta_description="Description",
        keywords=["old"],
        user_id=uuid.uuid4(),
    )
    db = FakeDb(blog)

    updated = controllers.update_blog(
        blog.id,
        UpdateBlogSchema(title="New title"),
        db,
        fake_user,
    )

    assert updated.title == "New title"
    assert db.committed is True
    assert db.refreshed is blog


class FakeDb:
    def __init__(self, blog):
        self.blog = blog
        self.committed = False
        self.refreshed = None

    def get(self, model, id):
        if model is BlogModel and id == self.blog.id:
            return self.blog
        return None

    def add(self, instance):
        pass

    def commit(self):
        self.committed = True

    def refresh(self, instance):
        self.refreshed = instance
