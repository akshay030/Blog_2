from pydantic import BaseModel
from src.users.models import UserRole
import uuid
from datetime import datetime

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.READER
    
    
class UserResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    role: UserRole
    created_at: datetime
    
class LoginSchema(BaseModel):
    email:str
    password:str
    
    
class LoginResponseSchema(BaseModel):
    access_token:str
    token_type:str
    user:UserResponseSchema
    
class IsAuthResponseSchema(BaseModel):
    authenticated: bool
    user: UserResponseSchema