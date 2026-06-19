import uuid

from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from src.utils.timestamps import TimestampMixin
from src.utils.db import Base


class CommentModel(TimestampMixin, Base):
    __tablename__ = "comment_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    comment = Column(Text)
    blog_id = Column(UUID, ForeignKey("blog_table.id", ondelete="CASCADE"))
    user_id = Column(UUID, ForeignKey("user_table.id", ondelete="CASCADE"))
