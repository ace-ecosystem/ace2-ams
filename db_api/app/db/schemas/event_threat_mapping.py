from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_threat_mapping = Table(
    "event_threat_mapping",
    Base.metadata,
    Column(
        "event_uuid",
        UUID(as_uuid=True),
        ForeignKey("event.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "threat_uuid",
        UUID(as_uuid=True),
        ForeignKey("threat.uuid"),
        index=True,
        primary_key=True,
    ),
)
