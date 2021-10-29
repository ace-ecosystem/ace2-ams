from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_prevention_tool_mapping = Table(
    "event_prevention_tool_mapping",
    Base.metadata,
    Column(
        "event_uuid",
        UUID(as_uuid=True),
        ForeignKey("event.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "prevention_tool_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_prevention_tool.uuid"),
        primary_key=True,
    ),
)
