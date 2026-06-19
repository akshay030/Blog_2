import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey,Integer,Float

from sqlalchemy.dialects.postgresql import UUID

from src.utils.db import Base
from src.utils.timestamps import TimestampMixin


class AuditLogModel(
    TimestampMixin,
    Base
):
    __tablename__ = "audit_log_table"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "user_table.id",
            ondelete="CASCADE"
        )
    )

    action = Column(
        String,
        nullable=False
    )

    resource = Column(
        String,
        nullable=False
    )

    resource_id = Column(
        UUID(as_uuid=True)
    )
    
class ApiRequestLogModel(
    TimestampMixin,
    Base
):
    __tablename__ = "api_request_log_table"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    method = Column(String)

    path = Column(String)

    status_code = Column(Integer)

    response_time = Column(Float)
    