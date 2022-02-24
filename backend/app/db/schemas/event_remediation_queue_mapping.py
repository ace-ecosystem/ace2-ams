from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_remediation_queue_mapping = Table(
    "event_remediation_queue_mapping",
    Base.metadata,
    Column(
        "event_remediation_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_remediation.uuid", ondelete="CASCADE"),
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
