import uuid
from enum import Enum

from sqlalchemy import Column, String,ForeignKey,JSON,Text
from sqlalchemy.dialects.postgresql import UUID
from src.utils.timestamps import TimestampMixin
from src.utils.db import Base



class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"


# class BlogModel(TimestampMixin,Base):
#     __tablename__ = "blog_table"

#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4
#     )

#     title = Column(String, nullable=False)
#     introduction = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     conclusion = Column(String)
#     user_id = Column(UUID, ForeignKey("user_table.id",ondelete="CASCADE"))
    
class BlogModel(TimestampMixin, Base):
    __tablename__ = "blog_table"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(String)

    introduction = Column(Text)

    content = Column(Text)

    conclusion = Column(Text)

    slug = Column(String, unique=True, nullable=False)

    meta_description = Column(String(160))

    keywords = Column(JSON)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_table.id", ondelete="CASCADE")
    )