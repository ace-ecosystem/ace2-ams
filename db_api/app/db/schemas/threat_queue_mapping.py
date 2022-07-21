from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


threat_queue_mapping = Table(
    "threat_queue_mapping",
    Base.metadata,
    Column(
        "threat_uuid",
        UUID(as_uuid=True),
        ForeignKey("threat.uuid", ondelete="CASCADE"),
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
