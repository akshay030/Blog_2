from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

# schemas.py


class BlogSchema(BaseModel):
    title: str
    introduction: str
    content: str
    conclusion: str

    slug: str
    meta_description: str
    keywords: list[str]


class UpdateBlogSchema(BaseModel):
    title: str | None = None
    introduction: str | None = None
    content: str | None = None
    conclusion: str | None = None

    slug: str | None = None
    meta_description: str | None = None
    keywords: list[str] | None = None


class BlogResponseSchema(BaseModel):

    id: uuid.UUID

    title: str

    introduction: str

    content: str

    conclusion: str

    slug: str | None = None

    meta_description: str | None = None

    keywords: list[str] | None = None

    user_id: uuid.UUID

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# class ImproveBlogSchema(BaseModel):
#     title: str

#     introduction: str

#     content: str

#     conclusion: str

#     audience: str

#     tone: str


# class ImprovedBlogResponseSchema(BaseModel):
#     title: str

#     introduction: str

#     content: str

#     conclusion: str

#     score: float
