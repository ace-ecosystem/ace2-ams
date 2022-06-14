from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_tag_mapping = Table(
    "event_tag_mapping",
    Base.metadata,
    Column(
        "event_uuid",
        UUID(as_uuid=True),
        ForeignKey("event.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "tag_uuid",
        UUID(as_uuid=True),
        ForeignKey("tag.uuid"),
        index=True,
        primary_key=True,
    ),
)
