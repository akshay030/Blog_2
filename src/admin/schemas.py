from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel
from src.users.models import UserRole
import uuid

class DashboardStatsSchema(BaseModel):
    total_users: int
    total_blogs: int
    total_comments: int

    total_admins: int
    total_authors: int
    total_readers: int

class AuditLogResponseSchema(BaseModel):

    action: str
    resource: str
    resource_id: str | None

    created_at: datetime

    class Config:
        from_attributes = True
        
class UserListSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True
 
class MessageSchema(BaseModel):
    message: str
           
class UpdateRoleSchema(BaseModel):
    role: UserRole
    
class ApiStatsResponseSchema(BaseModel):

    total_requests: int

    success_requests: int

    failed_requests: int

    avg_response_time: float
    
class ApiLogSchema(BaseModel):

    user_id: uuid.UUID | None

    method: str

    path: str

    status_code: int

    response_time: float

    created_at: datetime

    class Config:
        from_attributes = True
        
class RecentActivitySchema(BaseModel):

    action: str

    resource: str

    resource_id: uuid.UUID | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    
class TopEndpointSchema(BaseModel):

    path: str

    count: int
    
class ActiveUserSchema(BaseModel):

    user_id: uuid.UUID

    request_count: int
    
class FailedRequestSchema(BaseModel):

    status_code: int

    count: int