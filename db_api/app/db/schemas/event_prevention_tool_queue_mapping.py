from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_prevention_tool_queue_mapping = Table(
    "event_prevention_tool_queue_mapping",
    Base.metadata,
    Column(
        "event_prevention_tool_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_prevention_tool.uuid", ondelete="CASCADE"),
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
