from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_risk_level_queue_mapping = Table(
    "event_risk_level_queue_mapping",
    Base.metadata,
    Column(
        "event_risk_level_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_risk_level.uuid", ondelete="CASCADE"),
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
