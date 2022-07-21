from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_vector_mapping = Table(
    "event_vector_mapping",
    Base.metadata,
    Column(
        "event_uuid",
        UUID(as_uuid=True),
        ForeignKey("event.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "vector_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_vector.uuid"),
        index=True,
        primary_key=True,
    ),
)
