from pydantic import BaseModel
from datetime import datetime
import uuid


class ProfileSchema(BaseModel):
    bio: str


class UpdateProfileSchema(BaseModel):
    bio: str | None = None


class ProfileResponseSchema(BaseModel):

    id: uuid.UUID
    bio: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
