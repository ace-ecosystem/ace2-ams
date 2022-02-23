from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


node_threat_queue_mapping = Table(
    "node_threat_queue_mapping",
    Base.metadata,
    Column(
        "node_threat_uuid",
        UUID(as_uuid=True),
        ForeignKey("node_threat.uuid", ondelete="CASCADE"),
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
