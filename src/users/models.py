import uuid
from enum import Enum

from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from src.utils.timestamps import TimestampMixin
from src.utils.db import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"


class UserModel(TimestampMixin,Base):
    __tablename__ = "user_table"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)

    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.READER
    )