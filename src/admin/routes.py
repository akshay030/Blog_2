from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from src.admin.schemas import AuditLogResponseSchema
from src.utils.db import get_db
from src.utils.permissions import require_roles

from src.users.models import UserRole
from src.admin.schemas import FailedRequestSchema,ActiveUserSchema,TopEndpointSchema,RecentActivitySchema,ApiLogSchema,ApiStatsResponseSchema,DashboardStatsSchema,AuditLogResponseSchema,UserListSchema,UpdateRoleSchema,MessageSchema
from src.admin import controllers
import uuid


admin_routes = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@admin_routes.get(
    "/dashboard",
    response_model=DashboardStatsSchema
)
def dashboard(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.dashboard_stats(db)


@admin_routes.get(
    "/logs",
    response_model=list[AuditLogResponseSchema]
)
def logs(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.get_logs(
        db,
        limit,
        offset
    )
    
@admin_routes.get(
    "/users",
    response_model=list[UserListSchema]
)
def users(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.get_users(
        db,
        None,
        limit,
        offset
    )
    
@admin_routes.get(
    "/users/{user_id}",
    response_model=UserListSchema
)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.get_user(
        db,
        user_id
    )
    
@admin_routes.patch(
    "/users/{user_id}/role",
    response_model=UserListSchema
)
def update_role(
    user_id: uuid.UUID,
    body: UpdateRoleSchema,
    db: Session = Depends(get_db),
    admin=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return controllers.update_role(
        db=db,
        user_id=user_id,
        role=body.role,
        admin_id=admin.id
    )
    
@admin_routes.delete(
    "/users/{user_id}",
    response_model=MessageSchema
)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.delete_user(
        db=db,
        user_id=user_id,
        admin_id=admin.id
    )
    
@admin_routes.get(
    "/api-stats",
    response_model=ApiStatsResponseSchema
)
def api_stats(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.api_stats(db)


@admin_routes.get(
    "/api-logs",
    response_model=list[ApiLogSchema]
)
def api_logs(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.get_api_logs(
        db=db,
        limit=limit,
        offset=offset
    )
    
    
@admin_routes.get(
    "/recent-activity",
    response_model=list[RecentActivitySchema]
)
def recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.recent_activity(
        db,
        limit
    )
    
@admin_routes.get(
    "/top-endpoints",
    response_model=list[TopEndpointSchema]
)
def top_endpoints(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.top_endpoints(db)

@admin_routes.get(
    "/most-active-users",
    response_model=list[ActiveUserSchema]
)
def most_active_users(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.most_active_users(db)

@admin_routes.get(
    "/failed-requests",
    response_model=list[FailedRequestSchema]
)
def failed_requests(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return controllers.failed_requests(db)