from sqlalchemy import func

from src.users.models import UserModel, UserRole
from src.blogs.models import BlogModel
from src.comments.models import CommentModel
from src.admin.models import AuditLogModel,ApiRequestLogModel
from fastapi import HTTPException


def dashboard_stats(db):

    total_users = db.query(func.count(UserModel.id)).scalar()

    total_blogs = db.query(func.count(BlogModel.id)).scalar()

    total_comments = db.query(func.count(CommentModel.id)).scalar()

    total_admins = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.role == UserRole.ADMIN)
        .scalar()
    )

    total_authors = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.role == UserRole.AUTHOR)
        .scalar()
    )

    total_readers = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.role == UserRole.READER)
        .scalar()
    )

    return {
        "total_users": total_users,
        "total_blogs": total_blogs,
        "total_comments": total_comments,
        "total_admins": total_admins,
        "total_authors": total_authors,
        "total_readers": total_readers,
    }

def create_audit_log(db, user_id, action, resource, resource_id=None):

    log = AuditLogModel(
        user_id=user_id, action=action, resource=resource, resource_id=resource_id
    )

    db.add(log)
    db.commit()

def get_logs(db, limit: int = 20, offset: int = 0):

    return (
        db.query(AuditLogModel)
        .order_by(AuditLogModel.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def get_users(db, search: str | None = None, limit: int = 10, offset: int = 0):
    return db.query(UserModel).offset(offset).limit(limit).all()

def get_user(db, user_id):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_role(db, user_id, role, admin_id):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role

    db.commit()
    db.refresh(user)

    create_audit_log(
        db=db,
        user_id=admin_id,
        action="ROLE_UPDATED",
        resource="USER",
        resource_id=str(user.id),
    )

    return user

def total_users(db):

    return db.query(func.count(UserModel.id)).scalar()

def delete_user(db, user_id, admin_id):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    create_audit_log(
        db=db,
        user_id=admin_id,
        action="USER_DELETED",
        resource="USER",
        resource_id=str(user_id),
    )

    return {"message": "User deleted successfully"}

def create_api_log(db, user_id, method, path, status_code, response_time):

    log = ApiRequestLogModel(
        user_id=user_id,
        method=method,
        path=path,
        status_code=status_code,
        response_time=response_time,
    )

    db.add(log)
    db.commit()

def api_stats(db):

    total_requests = db.query(func.count(ApiRequestLogModel.id)).scalar()

    success_requests = (
        db.query(func.count(ApiRequestLogModel.id))
        .filter(ApiRequestLogModel.status_code < 400)
        .scalar()
    )

    failed_requests = (
        db.query(func.count(ApiRequestLogModel.id))
        .filter(ApiRequestLogModel.status_code >= 400)
        .scalar()
    )

    avg_response_time = db.query(func.avg(ApiRequestLogModel.response_time)).scalar()

    return {
        "total_requests": total_requests,
        "success_requests": success_requests,
        "failed_requests": failed_requests,
        "avg_response_time": round(avg_response_time or 0, 3),
    }

def get_api_logs(db, status_code: int | None = None, limit: int = 20, offset: int = 0):
    query = db.query(ApiRequestLogModel)

    if status_code:
        query = query.filter(ApiRequestLogModel.status_code == status_code)

    return (
        query.order_by(ApiRequestLogModel.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def recent_activity(db, limit: int = 10):

    return (
        db.query(AuditLogModel)
        .order_by(AuditLogModel.created_at.desc())
        .limit(limit)
        .all()
    )

def top_endpoints(db):

    result = (
        db.query(
            ApiRequestLogModel.path, func.count(ApiRequestLogModel.id).label("count")
        )
        .group_by(ApiRequestLogModel.path)
        .order_by(func.count(ApiRequestLogModel.id).desc())
        .limit(10)
        .all()
    )

    return [{"path": row.path, "count": row.count} for row in result]

def most_active_users(db):

    result = (
        db.query(
            ApiRequestLogModel.user_id,
            func.count(ApiRequestLogModel.id).label("request_count"),
        )
        .filter(ApiRequestLogModel.user_id.isnot(None))
        .group_by(ApiRequestLogModel.user_id)
        .order_by(func.count(ApiRequestLogModel.id).desc())
        .limit(10)
        .all()
    )

    return [
        {"user_id": str(row.user_id), "request_count": row.request_count}
        for row in result
    ]

def failed_requests(db):

    result = (
        db.query(
            ApiRequestLogModel.status_code,
            func.count(ApiRequestLogModel.id).label("count"),
        )
        .filter(ApiRequestLogModel.status_code >= 400)
        .group_by(ApiRequestLogModel.status_code)
        .order_by(func.count(ApiRequestLogModel.id).desc())
        .all()
    )

    return [{"status_code": row.status_code, "count": row.count} for row in result]
