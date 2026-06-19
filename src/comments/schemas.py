from pydantic import BaseModel
import uuid


class CommentSchema(BaseModel):
    comment: str


class CommentResponseSchema(BaseModel):
    id: uuid.UUID
    comment: str
    blog_id: uuid.UUID
    user_id: uuid.UUID
    name: str
