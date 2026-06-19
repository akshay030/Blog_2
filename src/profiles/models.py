import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.utils.timestamps import TimestampMixin
from src.utils.db import Base


class ProfileModel(TimestampMixin, Base):
    __tablename__ = "profile_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    bio = Column(String, default="")

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user_table.id", ondelete="CASCADE"), unique=True
    )
