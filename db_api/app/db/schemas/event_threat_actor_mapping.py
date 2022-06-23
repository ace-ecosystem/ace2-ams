from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_threat_actor_mapping = Table(
    "event_threat_actor_mapping",
    Base.metadata,
    Column(
        "event_uuid",
        UUID(as_uuid=True),
        ForeignKey("event.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "threat_actor_uuid",
        UUID(as_uuid=True),
        ForeignKey("threat_actor.uuid"),
        index=True,
        primary_key=True,
    ),
)
