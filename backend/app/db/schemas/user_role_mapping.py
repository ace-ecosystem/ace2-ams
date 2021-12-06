from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


user_role_mapping = Table(
    "user_role_mapping",
    Base.metadata,
    Column(
        "user_uuid",
        UUID(as_uuid=True),
        ForeignKey("user.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "user_role_uuid",
        UUID(as_uuid=True),
        ForeignKey("user_role.uuid"),
        index=True,
        primary_key=True,
    ),
)
