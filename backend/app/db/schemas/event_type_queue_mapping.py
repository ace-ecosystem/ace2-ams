from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_type_queue_mapping = Table(
    "event_type_queue_mapping",
    Base.metadata,
    Column(
        "event_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_type.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "queue_uuid",
        UUID(as_uuid=True),
        ForeignKey("queue.uuid"),
        index=True,
        primary_key=True,
    ),
)
