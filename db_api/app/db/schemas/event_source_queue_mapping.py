from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_source_queue_mapping = Table(
    "event_source_queue_mapping",
    Base.metadata,
    Column(
        "event_source_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_source.uuid", ondelete="CASCADE"),
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
