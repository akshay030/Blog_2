import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.admin import controllers
from src.users.models import UserModel, UserRole


def test_get_user_raises_404_when_user_missing():
    db = QueryDb(user=None)

    with pytest.raises(HTTPException) as exc:
        controllers.get_user(db, uuid.uuid4())

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


def test_update_role_changes_user_role_and_writes_audit_log(monkeypatch):
    user = SimpleNamespace(id=uuid.uuid4(), role=UserRole.READER)
    admin_id = uuid.uuid4()
    audit_calls = []
    db = QueryDb(user=user)

    monkeypatch.setattr(
        "src.admin.controllers.create_audit_log",
        lambda **kwargs: audit_calls.append(kwargs),
    )

    updated = controllers.update_role(db, user.id, UserRole.AUTHOR, admin_id)

    assert updated.role == UserRole.AUTHOR
    assert db.committed is True
    assert db.refreshed is user
    assert audit_calls == [
        {
            "db": db,
            "user_id": admin_id,
            "action": "ROLE_UPDATED",
            "resource": "USER",
            "resource_id": str(user.id),
        }
    ]


def test_api_stats_rounds_average_response_time():
    db = ApiStatsDb(
        total_requests=3,
        success_requests=2,
        failed_requests=1,
        avg_response_time=0.4567,
    )

    result = controllers.api_stats(db)

    assert result == {
        "total_requests": 3,
        "success_requests": 2,
        "failed_requests": 1,
        "avg_response_time": 0.457,
    }


class QueryDb:
    def __init__(self, user):
        self.user = user
        self.committed = False
        self.refreshed = None

    def query(self, model):
        assert model is UserModel
        return self

    def filter(self, *args):
        return self

    def first(self):
        return self.user

    def commit(self):
        self.committed = True

    def refresh(self, instance):
        self.refreshed = instance


class ApiStatsDb:
    def __init__(
        self,
        total_requests,
        success_requests,
        failed_requests,
        avg_response_time,
    ):
        self.values = [
            total_requests,
            success_requests,
            failed_requests,
            avg_response_time,
        ]

    def query(self, *args):
        return ApiStatsQuery(self.values.pop(0))


class ApiStatsQuery:
    def __init__(self, value):
        self.value = value

    def filter(self, *args):
        return self

    def scalar(self):
        return self.value
